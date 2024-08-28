#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:

Test case to test the functionality of list_snapshot in the PSL
"""

from infra_utils.san_test import SanTest
from infra_utils.utils.san_utils import SanUtils


class TestCase(SanTest):

    """
    Test case to verify the functionality of list_snapshot
    Ref: INFRA:SAN Snapshot 17
    http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%17

    :Jira          Story OSS-70673
    :Requirement   ID: OSS-70673
    :Title:        List all snapshots on the LUN using PSL get_snapshots
    :Description:  Positive test case to list all snapshots on the LUN using
                   PSL get_snapshots(<lun_name>)
    :PreCondition: At least the following snapshots must exist in the Pool
                   -LUN 1 <LUN 1 Name>_snapshot_A,<LUN 1 Name>_snapshot_B
                   -LUN 2 <LUN 2 Name>_snapshot_C
    :TestStep:     1: Using sanapitest.py, call get_snapshots() with the LUN
                      that has two snapshots on it
                   1.1 Verify the standard out lists only those two snapshots
                   1.2 Verify there is no error output
    """

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        #create 2 testing luns
        self.lun_name1 = "test_lun_OSS70673_17_1"
        self.lun_name2 = "test_lun_OSS70673_17_2"
        self.snap_names = ["test_lun_OSS70673_17_1_snap1",
                      "test_lun_OSS70673_17_1_snap2",
                      "test_lun_OSS70673_17_2_snap1"]
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
        Test cases list snapshots on one particular lun
        """
        self.create_luns_for_testing([self.lun_name1, self.lun_name2])

        #create 2 snaps on the first lun and one on the second lun

        result = self.sanapi_create_snapshot(self.snap_names[0], self.lun_name1)
        if result.retcode != 0:
            self.fail("Unable to create snapshot {0}".format(self.snap_names[0]))
        result = self.sanapi_create_snapshot(self.snap_names[1], self.lun_name1)
        if result.retcode != 0:
            self.fail("Unable to create snapshot {0}".format(self.snap_names[1]))
        result = self.sanapi_create_snapshot(self.snap_names[2], self.lun_name2)
        if result.retcode != 0:
            self.fail("Unable to create snapshot {0}".format(self.snap_names[2]))

        #list snapshots on LUN 1 via the PSL 
        psl_snaps = self.sanapi_list_snapshots_one_lun(self.lun_name1)

        #get the snapshots on LUN 1 via the navisec code directly
        navi_snaps = self.navi_list_snaps_one_lun(self.lun_name1)

        #first check PSL returned the two snapshots created
        found_list = 0
        if self.snap_names[0] in psl_snaps.keys():
               found_list += 1
        if self.snap_names[1] in psl_snaps.keys():
               found_list += 1
        self.assertEquals(found_list, 2)        

        #verify that snap_name and lun_name returned are correct (first snap)
        snap_details = psl_snaps[self.snap_names[0]]
        self.assertEquals(snap_details['snapshot name'], self.snap_names[0])
        self.assertEquals(snap_details['resource lun name'], self.lun_name1)

        #verify that snap_name and lun_name returned are correct (second snap)
        snap_details = psl_snaps[self.snap_names[1]]
        self.assertEquals(snap_details['snapshot name'], self.snap_names[1])
        self.assertEquals(snap_details['resource lun name'], self.lun_name1)

        self.assertEquals(len(psl_snaps), len(navi_snaps))

if __name__ == '__main__':
    TestCase().run_test()
