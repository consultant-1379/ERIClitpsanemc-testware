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
    Ref: INFRA:SAN Snapshot 16
    http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%16

    :Jira          Story OSS-70673
    :Requirement   ID: OSS-70673
    :Title:        List all snapshots on the array using PSL get_snapshots
    :Description:  Positive test case to list all snapshots on the array using
                   PSL get_snapshots()
    :PreCondition: At least the following snapshots must exist in the Pool
                   -LUN 1 <LUN 1 Name>_snapshot_A,<LUN 1 Name>_snapshot_B
                   -LUN 2 <LUN 2 Name>_snapshot_C
    :TestStep:     1: Using sanapitest.py, call get_snapshot() with no parameters
                   1.1 Verify the standard out lists all the snapshots in the array
                   1.2 Verify there is no error output
    """

    def setUp(self):
        """
        Set up the test case
        """
        self.lun_name1 = "test_lun_OSS70673_16_1"
        self.lun_name2 = "test_lun_OSS70673_16_2"
        self.snap_names = ["test_lun_OSS70673_16_1_snap1",
                           "test_lun_OSS70673_16_1_snap2",
                           "test_lun_OSS70673_16_2_snap1"]

        super(TestCase, self).setUp()
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
        Test case - list many snapshots
        """
        #create 2 testing luns
        self.create_luns_for_testing([self.lun_name1, self.lun_name2])

        result = self.sanapi_create_snapshot(self.snap_names[0], self.lun_name1)
        if result.retcode != 0:
            self.fail("Unable to create snapshot {0}".format(self.snap_names[0]))
        result = self.sanapi_create_snapshot(self.snap_names[1], self.lun_name1)
        if result.retcode != 0:
            self.fail("Unable to create snapshot {0}".format(self.snap_names[1]))
        result = self.sanapi_create_snapshot(self.snap_names[2], self.lun_name2)
        if result.retcode != 0:
            self.fail("Unable to create snapshot {0}".format(self.snap_names[2]))

        #list all snapshots via the PSL 
        psl_snaps = self.sanapi_list_snapshots()

        #list the snapshots via the navisec code directly
        navi_snaps = self.navi_get_snapshots()

        #ensure the PSL snaps returned include these three new ones
        found_list = 0
        for name in self.snap_names:
           if name in psl_snaps.keys():
               found_list += 1
        self.assertEquals(found_list, len(self.snap_names))

        #look at one snap and ensure that snap_name and lun_name are correct
        snap_details = psl_snaps[self.snap_names[2]]
        self.assertEquals(snap_details['snapshot name'], self.snap_names[2])
        self.assertEquals(snap_details['resource lun name'], self.lun_name2)

        #assert that the psl and navi list cmds return the same number of snaps
        self.assertEquals(len(navi_snaps), len(psl_snaps))

if __name__ == '__main__':
    TestCase().run_test()
