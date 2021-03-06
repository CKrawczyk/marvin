#!/usr/bin/env python
# encoding: utf-8

'''
Created by Brian Cherinka on 2016-04-28 14:07:58
Licensed under a 3-clause BSD license.

Revision History:
    Initial Version: 2016-04-28 14:07:58 by Brian Cherinka
    Last Modified On: 2016-04-28 14:07:58 by Brian

'''
from __future__ import print_function
from __future__ import division

from flask import Blueprint, render_template, request
from flask_classy import route
from marvin.core.exceptions import MarvinError
from marvin.tools.plate import Plate as mPlate
from marvin.utils.general import getImagesByPlate
from marvin.web.controllers import BaseWebView
from marvin.web.web_utils import buildImageDict
from marvin.api.base import arg_validate as av

plate = Blueprint("plate_page", __name__)


class Plate(BaseWebView):
    route_base = '/plate/'

    def __init__(self):
        ''' Initialize the route '''
        super(Plate, self).__init__('marvin-plate')
        self.plate = self.base.copy()
        self.plate['plateid'] = None

    def before_request(self, *args, **kwargs):
        ''' Do these things before a request to any route '''
        super(Plate, self).before_request(*args, **kwargs)
        self.reset_dict(self.plate)

    @route('/', methods=['GET', 'POST'])
    def index(self):

        return render_template('plate.html', **self.plate)

    def get(self, plateid):
        ''' Retrieve info for a given plate id '''

        # validate the input
        args = av.manual_parse(self, request)
        self.plate['plateid'] = args.get('plateid')
        pinputs = {'plateid': plateid, 'mode': 'local', 'nocubes': True, 'release': self._release}
        try:
            plate = mPlate(**pinputs)
        except MarvinError as e:
            self.plate['plate'] = None
            self.plate['drpver'] = self._drpver
            self.plate['error'] = 'Could not grab Plate for id {0}: {1}'.format(plateid, e)
        else:
            self.plate['plate'] = plate
            self.plate['drpver'] = plate._drpver
            tmpfile = plate._getFullPath(url=True)
            self.plate['sasurl'] = plate.platedir

        # Get images for plate
        imfiles = None
        try:
            imfiles = getImagesByPlate(plateid=plateid, as_url=True, mode='local', release=self._release)
        except MarvinError as e:
            self.plate['error'] = 'Error: could not get images for plate {0}: {1}'.format(plateid, e)
        else:
            # thumbs = [imfiles.pop(imfiles.index(t)) if 'thumb' in t else t for t in imfiles]
            # plateifu = ['-'.join(re.findall('\d{3,5}', im)) for im in imfiles]
            images = buildImageDict(imfiles)

        # if image grab failed, make placeholders
        if not imfiles:
            images = buildImageDict(imfiles, test=True, num=29)

        # Add images to dict
        self.plate['images'] = images

        return render_template('plate.html', **self.plate)


Plate.register(plate)
