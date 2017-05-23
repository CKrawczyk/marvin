/*
* @Author: Brian Cherinka
* @Date:   2016-05-13 13:26:21
* @Last Modified by:   Brian Cherinka
* @Last Modified time: 2017-05-22 15:58:36
*/

//jshint esversion: 6
'use strict';

class Search {

    // Constructor
    constructor() {
        this.searchform = $('#searchform');
        this.typeahead = $('#searchform .typeahead');
        this.returnparams = $('#returnparams');
        this.parambox = $('#parambox');
        this.searchbox = $("#searchbox");
    }

    // Print
    print() {
        console.log('I am Search!');
    }

    // Extract
    extractor(input) {
        let regexp = new RegExp('([^,]+)$');
        // parse input for newly typed text
        let result = regexp.exec(input);
        // select last entry after comma
        if(result && result[1]) {
            return result[1].trim();
        }
        return '';
    }

    // Initialize Query Param Typeahead
    initTypeahead(typediv, formdiv, url, fxn) {

        const _this = this;
        let typeurl;
        typediv = (typediv === undefined) ? this.typeahead : $(typediv);
        formdiv = (formdiv === undefined) ? this.searchform : $(formdiv);
        // get the typeahead search page getparams url
        try {
            typeurl = (url === undefined) ? Flask.url_for('search_page.getparams', {'paramdisplay':'best'}) : url;
        } catch (error) {
            Raven.captureException(error);
            console.error('Error getting search getparams url:',error);
        }
        const afterfxn = (fxn === undefined) ? null : fxn;

        function customQueryTokenizer(str) {
            let newstr = str.toString();
            return [_this.extractor(newstr)];
        };

        // create the bloodhound engine
        this.queryparams = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        //queryTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: customQueryTokenizer,
        prefetch: typeurl,
        remote: {
            url: typeurl,
            filter: (qpars)=>{ return qpars; }
        }
        });

        // initialize the bloodhound suggestion engine
        this.queryparams.initialize();

        // init the search typeahead
        typediv.typeahead('destroy');
        typediv.typeahead(
        {
        showHintOnFocus: true,
        items: 'all',
        source:this.queryparams.ttAdapter(),
        updater: function(item) {
            // used to updated the input box with selected option
            // item = selected item from dropdown
            let currenttext = this.$element.val();
            let removedtemptype = currenttext.replace(/[^,]*$/,'');
            let newtext = removedtemptype+item+', ';
            return newtext;
        },
        matcher: function (item) {
            // used to determined if a query matches an item
            let tquery = _this.extractor(this.query);
            console.log(tquery);
            if(!tquery) return false;
            return ~item.toLowerCase().indexOf(tquery.toLowerCase());
        },
        highlighter: function (item) {
          // used to highlight autocomplete results ; returns html
          let oquery = _this.extractor(this.query);
          let query = oquery.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&');
          return item.replace(new RegExp('(' + query + ')', 'ig'), function ($1, match) {
            return '<strong>' + match + '</strong>';
          });
        }
        });
    }
}
