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
    Ref: INFRA:SAN Snapshot 19
    http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%19

    :Jira          Story OSS-70673
    :Requirement   ID: OSS-70673
    :Title:        If no shapshot is found using PSL get_snapshots then an empty
                   list will be returned
    :Description:  Positive test case to verify that if no shapshot is found
                   using PSL get_snapshots() then an empty list will be returned
    :PreCondition: An existing LUN with no snapshots on it
    :TestStep:     1: Using sanapitest.py, call get_snapshot() with full
                      snapshot name of an existing snapshot
                   1.1 Verify the standard out lists only the specified snapshot
                   1.2 Verify there is no error output
    """

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()

        self.lun_name = "test_lun_OSS70673_19"
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
        Test case list snapshots on a lun where none exist
        """
        #create lun
        self.create_luns_for_testing([self.lun_name])

        #get nonexistant snapshot
        cmd = SanUtils.get_sanapitest_cmd(self.san['ip_a'], self.san['ip_b'],
              self.san['user'], self.san['password'], self.san['array_type'],
           ["--action=get_snapshots", "--lunname={0}".format(self.lun_name)])
        result = self.run_command(cmd, self.mws)
        self.assertEquals(result.retcode, 0)
        self.assertTrue("Empty List" in result.stdout)

        #ensure navisec command also returns no snapshots
        result1 = self.navi_list_snaps_one_lun(self.lun_name) 
        self.assertEquals(result1, [])

if __name__ == '__main__':
    TestCase().run_test()
