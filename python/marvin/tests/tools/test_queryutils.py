# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-05-24 18:27:50
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-05-28 15:17:28

from __future__ import print_function, division, absolute_import
from marvin.tools.query.query_utils import query_params, QueryParameter
import pytest
import itertools


@pytest.fixture(scope='session')
def data():
    groups = ['Metadata', 'Spaxel Metadata', 'Emission Lines', 'Kinematics', 'Spectral Indices', 'NSA Catalog']
    spaxelparams = ['spaxelprop.x', 'spaxelprop.y', 'spaxelprop.spx_snr']
    specindparams = ['spaxelprop.specindex_d4000']
    nsaparams = ['nsa.z', 'nsa.elpetro_logmass', 'nsa.elpetro_th50_r']
    data = {'groups': groups, 'spaxelmeta': spaxelparams, 'nsa': nsaparams, 'specind': specindparams}

    return data


class TestGroupList(object):

    def test_list_groups(self, data):
        groups = query_params.list_groups()
        assert data['groups'] == groups, 'groups should be the same'

    @pytest.mark.parametrize('name, result',
                             [('metadata', 'Metadata'),
                              ('spaxelmeta', 'Spaxel Metadata'),
                              ('emission', 'Emission Lines'),
                              ('kin', 'Kinematics'),
                              ('nsacat', 'NSA Catalog')])
    def test_get_group(self, name, result):
        group = query_params[name]
        assert result == group.name

    @pytest.mark.parametrize('name',
                             [('nsa catalog'),
                              ('NSA catalog'),
                              ('catalognsa'),
                              ('nsa--!catalgue'),
                              ('nsacat')])
    def test_different_keys(self, name):
        group = query_params[name]
        assert group.name == 'NSA Catalog'

    @pytest.mark.parametrize('groups', [(None), (['nsa']), (['specind', 'nsa']),
                                        (['spaxelmeta', 'specind'])])
    def test_list_params(self, data, groups):
        params = query_params.list_params(groups=groups)
        if not groups:
            myparams = data['spaxelmeta'] + data['nsa'] + data['specind']
        else:
            paramlist = [data[g] for g in groups]
            myparams = list(itertools.chain.from_iterable(paramlist))
        assert set(myparams).issubset(set(params))

    def test_raises_keyerror(self):
        errmsg = "meta is too ambiguous."
        with pytest.raises(KeyError) as cm:
            group = query_params['meta']
        assert cm.type == KeyError
        assert errmsg in str(cm.value)

    @pytest.mark.parametrize('name, result',
                             [('coord', None),
                              pytest.mark.xfail(raises=KeyError)(('meta', None))])
    def test_failure(self, name, result):
        res = query_params[name]
        assert result == res, 'result should be the same as res'


class TestParamList(object):

    @pytest.mark.parametrize('group, name, count', [('specind', 'Spectral Indices', 1),
                                                    ('kin', 'Kinematics', 6)])
    def test_get_paramgroup(self, group, name, count):
        assert group in query_params
        mygroup = query_params[group]
        othergroup = group == query_params
        assert type(mygroup) == type(othergroup)
        assert mygroup.name == othergroup.name
        assert mygroup.name == name
        assert len(mygroup) == count

    @pytest.mark.parametrize('group, param, name', [('specind', 'd4000', 'specindex_d4000')])
    def test_get_param(self, group, param, name):
        assert group in query_params
        assert param in query_params[group]
        myparam = param == query_params[group]
        assert myparam.name == name

    @pytest.mark.parametrize('group, param, ltype, expname',
                             [('kin', 'havel', None, None),
                              ('kin', 'havel', 'full', 'spaxelprop.emline_gvel_ha_6564'),
                              ('kin', 'havel', 'short', 'havel'),
                              ('kin', 'havel', 'display', 'Halpha Velocity')])
    def test_list_params(self, group, param, ltype, expname):
        kwargs = {ltype: True} if ltype else {}
        params = query_params[group].list_params(**kwargs)
        if not ltype:
            assert isinstance(params[0], QueryParameter)
        else:
            assert params[0] == expname

    @pytest.mark.parametrize('group, params, expset',
                             [('metadata', ['ra', 'dec'], ['cube.ra', 'cube.dec'])])
    def test_list_subset(self, group, params, expset):
        subset = query_params[group].list_params(params, full=True)
        assert set(expset) == set(subset)

    @pytest.mark.parametrize('groups, params1, params2, expset',
                             [(('metadata', 'nsa'), ['ra', 'dec'], ['z', 'absmag_g_r'],
                               ['cube.ra', 'cube.dec', 'nsa.z', 'nsa.elpetro_absmag_g_r'])])
    def test_join_two_list(self, groups, params1, params2, expset):
        group1, group2 = groups
        g1 = query_params[group1]
        g2 = query_params[group2]
        mylist = g1.list_params(params1, full=True) + g2.list_params(params2, full=True)
        assert set(expset) == set(mylist)

    def test_raises_keyerror(self):
        errmsg = "emline_gflux is too ambiguous."
        with pytest.raises(KeyError) as cm:
            param = query_params['emission']['emline_gflux']
        assert cm.type == KeyError
        assert errmsg in str(cm.value)


class TestQueryParams(object):

    @pytest.mark.parametrize('group, param, full, name, short, display',
                             [('nsa', 'z', 'nsa.z', 'z', 'z', 'Redshift'),
                              ('metadata', 'ra', 'cube.ra', 'ra', 'ra', 'RA'),
                              ('emission', 'gflux_ha', 'spaxelprop.emline_gflux_ha_6564', 'emline_gflux_ha_6564', 'haflux', 'Halpha Flux'),
                              ('spaxelmeta', 'x', 'spaxelprop.x', 'x', 'x', 'Spaxel X')])
    def test_query_param(self, group, param, full, name, short, display):
        par = query_params[group][param]
        assert par.full == full
        assert par.name == name
        assert par.short == short
        assert par.display == display

