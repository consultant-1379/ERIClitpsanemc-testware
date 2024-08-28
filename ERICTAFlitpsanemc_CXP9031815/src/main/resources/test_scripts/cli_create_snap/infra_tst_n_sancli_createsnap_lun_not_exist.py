#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/
    infra_tst_n_sancli_createsnap_lun_not_exist
:Requirement   ID: OSS-77967
:TestCaseID:   infra_tst_n_sancli_createsnap_lun_not_exist
:Title:        Create a snapshot of a non-existent LUN name
:Description:  Negative test case to create snapshot of non-existent LUN name
:PreCondition: -
:Type:         Functional test case
:TestStep:     1: Assert the output contains errors (sancli.py returns 1)
               2: Assert there is an explanatory error message logged
"""
from infra_utils.san_test import SanTest
from ptaf.utils.litp_cmd_utils import LitpUtils

class TestCase(SanTest):

    def setUp(self):
        """
        Setup the test
        """
        super(TestCase, self).setUp()
        self.sanapi_target = self.mws
        self.navi_target = self.mws

        self.test_lun_names = ['nowaythislunexists']
        self.snap_name="test_lun77967_vandals1"
        luns = self.navi_get_luns()
        self.assertFalse(self.test_lun_names[0] in luns)

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Create a snapshot of non-existing LUN
        Actions:
            1: Assert the output contains errors
            2: Assert the output contains sufficient error message
                when non-existing LUN is used
        """
        # Use NAVI command to verify that the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

        cmd = self.sancli_create_snapshot(self.snap_name,self.test_lun_names[0])
        self.assertTrue(cmd.retcode == 1)
        self.assertTrue("The (pool lun) may not exist" in cmd.stdout)

        # Use NAVI command to verify that the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

if __name__ == '__main__':
    TestCase().run_test()
