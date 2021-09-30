from ..workflow.epi_isl.epi_isl_helpers import parse_gisaid_num


def test_parse_gisaid_num():
    gisaid_one = {"Virus name":"hCoV-19/USA/KS-KHEL-0002/2021"}
    gisaid_two = {"Virus name":"hCoV-19/USA/KS-KHEL-9999/2020"}
    gisaid_three = {"Virus name":"hCoV-19/USA/KS-KHEL-1645/2021"}
    gisaid_four = {"Virus name":"hCoV-19/USA/KS-KHEL-2299/1645"}
    gisaid_five = {"Virus name":"hCoV-19/USA/KS-KHEL-8164/0000"}
    gisaid_six = {"Virus name":"hCoV-19/USA/KS-KHEL-0000/2018"}
    gisaid_seven = {"Virus name":"hCoV-19/US/KS-KHEL-0000/2018"}
    gisaid_eight = {"Virus "}
    assert parse_gisaid_num(gisaid_one) == 2
    assert parse_gisaid_num(gisaid_two) == 9999
    assert parse_gisaid_num(gisaid_three) == 1645
    assert parse_gisaid_num(gisaid_four) == 2299
    assert parse_gisaid_num(gisaid_five) == 8164
    assert parse_gisaid_num(gisaid_six) == 0
    assert parse_gisaid_num(gisaid_seven) == None
    assert parse_gisaid_num(gisaid_eight) == None






