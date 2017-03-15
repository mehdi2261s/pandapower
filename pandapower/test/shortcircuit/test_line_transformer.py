# -*- coding: utf-8 -*-

__author__ = 'lthurner'

import pytest
import pandapower.shortcircuit as sc
import pandapower as pp

@pytest.fixture
def net_transformer():
    net = pp.create_empty_network(sn_kva=2e3)
    b1a = pp.create_bus(net, vn_kv=10.)
    b1b = pp.create_bus(net, vn_kv=10.)
    b2 = pp.create_bus(net, vn_kv=.4)
    pp.create_bus(net, vn_kv=0.4, in_service=False) #add out of service bus to test oos indexing
    pp.create_ext_grid(net, b1a, s_sc_max_mva=100., s_sc_min_mva=40., rx_min=0.1, rx_max=0.1)
    pp.create_switch(net, b1a, b1b, et="b")
    pp.create_transformer_from_parameters(net, b1b, b2, vn_hv_kv=11., vn_lv_kv=0.42, vsc_percent=6.,
                                          vscr_percent=0.5, pfe_kw=1.4, shift_degree=0.0,
                                          tp_side="hv", tp_mid=0, tp_min=-2, tp_max=2, tp_pos=2,
                                          tp_st_percent=2.5, parallel=2, sn_kva=400, i0_percent=0.5)
    pp.create_shunt(net, b2, q_kvar=500, p_kw=500) #adding a shunt shouldn't change the result
    return net
  
def test_max_10_one_line_one_transformer(net_transformer):
    net = net_transformer
    sc.runsc(net, case='max', ip=True, ith=True, lv_tol_percent= 10.)
    assert (abs(net.res_bus_sc.ikss_ka.at[0] - 5.77350301940194) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[1] - 5.77350301940194) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[2] - 16.992258758) <1e-5)
     
    assert (abs(net.res_bus_sc.ip_ka.at[0] - 14.25605) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[1] - 14.25605) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[2] - 42.739927153) <1e-5)    
    
    assert (abs(net.res_bus_sc.ith_ka.at[0] - 5.8711913689) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[1] - 5.8711913689) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[2] - 17.328354145) <1e-5)

def test_max_6_one_line_one_transformer(net_transformer):
    net = net_transformer
    sc.runsc(net, case='max', ip=True, ith=True, lv_tol_percent = 6.)
    assert (abs(net.res_bus_sc.ikss_ka.at[0] - 5.77350301940194) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[1] - 5.77350301940194) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[2] - 16.905912296) <1e-5)  
      
    assert (abs(net.res_bus_sc.ip_ka.at[0] - 14.256046241) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[1] - 14.256046241) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[2] - 42.518706441) <1e-5)
    
    assert (abs(net.res_bus_sc.ith_ka.at[0] - 5.8711913689) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[1] - 5.8711913689) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[2] - 17.240013111) <1e-5)
    
def test_min_10_one_line_one_transformer(net_transformer):
    net = net_transformer
    sc.runsc(net, case='min', ip=True, ith=True, lv_tol_percent= 10.)
    assert (abs(net.res_bus_sc.ikss_ka.at[0] - 2.309401) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[1] - 2.309401) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[2] - 12.912468695) <1e-5)
        
    assert (abs(net.res_bus_sc.ip_ka.at[0] - 5.702418) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[1] - 5.702418) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[2] - 32.405489528) <1e-5)    
    
    assert (abs(net.res_bus_sc.ith_ka.at[0] - 2.348476) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[1] - 2.348476) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[2] - 13.162790807) <1e-5)

def test_min_6_one_line_one_transformer(net_transformer):
    net = net_transformer
    sc.runsc(net, case='min', ip=True, ith=True, lv_tol_percent = 6.)
    assert (abs(net.res_bus_sc.ikss_ka.at[0] - 2.309401) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[1] - 2.309401) <1e-5)
    assert (abs(net.res_bus_sc.ikss_ka.at[2] - 13.39058012) <1e-5)
        
    assert (abs(net.res_bus_sc.ip_ka.at[0] - 5.702418) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[1] - 5.702418) <1e-5)
    assert (abs(net.res_bus_sc.ip_ka.at[2] - 33.599801499) <1e-5)    
    
    assert (abs(net.res_bus_sc.ith_ka.at[0] - 2.348476) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[1] - 2.348476) <1e-5)
    assert (abs(net.res_bus_sc.ith_ka.at[2] - 13.649789214) <1e-5)

if __name__ == '__main__':
    pytest.main(["test_line_transformer.py"])
