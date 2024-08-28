#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:

Test cases to test the functionality of list_snapshot in the PSL
"""

from infra_utils.san_test import SanTest
from infra_utils.utils.san_utils import SanUtils


class TestCase(SanTest):
    """
    Test case to verify the functionality of list_snapshot
    Ref: INFRA:SAN Snapshot 20
    http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%20

    :Jira          Story OSS-70673
    :Requirement   ID: OSS-70673
    :Title:        If no shapshot is found in PSL get_snapshot(), then an error
                   is thrown
    :Description:  Negative test case to verify that if no shapshot is found in
                   PSL get_snapshot(), then an error is thrown
    :PreCondition: At least the following must exist
                   -LUN 1 where LUN1 has no shapshots
    :TestStep:     1: Using sanapitest.py, call get_snapshot() with the name
                      of a snapshot that doesn't exist
                   1.1 Verify the output contains a sufficient error message
    """

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()

        self.lun_name = "test_lun_OSS70673_20_1"
        self.snap_name = "test_lun_OSS70673_20_1_snap1"
        self.sanapi_target = self.mws
        self.navi_target = self.mws

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Test case list a snapshot which doesn't exist
        """
        #create lun
        self.create_luns_for_testing([self.lun_name])

        #get nonexistant snapshot
        cmd = SanUtils.get_sanapitest_cmd(self.san['ip_a'], self.san['ip_b'],
              self.san['user'], self.san['password'], self.san['array_type'],
            ["--action=get_snapshot", "--snap_name={0}".format(self.snap_name)])
        result = self.run_command(cmd, self.mws)
        self.assertTrue("Could not retrieve the specified (Snapshot)" in result.stdout)

        result1 = self.navi_list_one_snap(format(self.snap_name))
        self.assertTrue(result1.retcode != 0)

if __name__ == '__main__':
    TestCase().run_test()
