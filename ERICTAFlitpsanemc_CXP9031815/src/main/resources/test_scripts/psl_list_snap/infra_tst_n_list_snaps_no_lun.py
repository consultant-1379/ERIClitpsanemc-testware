#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:

Test cases to test the functionality of list_snapshot in the PSL
"""

from infra_utils.san_test import SanTest
from infra_utils.utils.san_utils import SanUtils
from time import mktime, localtime


class TestCase(SanTest):
    """
    Test case to verify the functionality of list_snapshot
    Ref: INFRA:SAN Snapshot 21
    http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%21

    :Jira          Story OSS-70673
    :Requirement   ID: OSS-70673
    :Title:        List snapshot of non-existing LUN name (using PSL)
    :Description:  Negative test case to list a snapshot of non-exting LUN
    :PreCondition: None
    :TestStep:     1: Attempt to list snapshots of a LUN that doesn't exist
                   2: Verify the output contains a sufficient error message
    """

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        self.lun_name = "test_lun_OSS70673_21"
        self.sanapi_target = self.mws
        self.navi_target = self.mws

    def tearDown(self):
        """
        Clean up after the test case
        """
        super(TestCase, self).tearDown()

    def test(self):
        """
        Test case list snaps on a nonexistant lun
        """

        cmd = SanUtils.get_sanapitest_cmd(self.san['ip_a'], self.san['ip_b'],
                                      self.san['user'], self.san['password'],
                                                      self.san['array_type'],
           ["--action=get_snapshots", "--lunname={0}".format(self.lun_name)])
        result = self.run_command(cmd, self.mws)
        self.assertTrue(result.retcode > 0)
        self.assertTrue("Exception" in result.stdout)

        # now make sure you get the same result independently
        snaps = self.navi_list_snaps_one_lun(self.lun_name)
        self.assertEquals(snaps, [])

if __name__ == '__main__':
    TestCase().run_test()
