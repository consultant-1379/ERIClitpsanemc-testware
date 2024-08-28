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
    Ref: INFRA:SAN Snapshot 18
    http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%18

    :Jira          Story OSS-70673
    :Requirement   ID: OSS-70673
    :Title:        Get a specific snapshot using PSL get_snapshot
    :Description:  Positive test case to get a specific snapshot
    :PreCondition: At least the following snapshots must exist in the Pool
                   -LUN 1 <LUN 1 Name>_snapshot_A,<LUN 1 Name>_snapshot_B
                   -LUN 2 <LUN 2 Name>_snapshot_C
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
        self.lun_name = "test_lun_OSS70673_18"
        self.snap_name = "test_lun_OSS70673_18_snap1"
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
        List one specific snapshot on a lun
        """

        self.create_luns_for_testing([self.lun_name])

        #create a snapshot of this new lun
        result = self.sanapi_create_snapshot(self.snap_name, self.lun_name)
        if result.retcode != 0:
            self.fail('Unable to create snapshot {0}'.format(self.snap_name))

        #list the snapshot using the PSL and assert the correct one is returned
        snap = self.sanapi_get_snapshot(self.snap_name)
        self.assertTrue(self.snap_name in snap.keys())
        self.assertTrue(snap != [])
        self.assertEquals(len(snap), 1)

        #further verification that snap_name and lun_name returned are correct
        snap_details = snap[self.snap_name]
        self.assertEquals(snap_details['snapshot name'], self.snap_name)
        self.assertEquals(snap_details['resource lun name'], self.lun_name)

        #now list the snapshot using navisec and assert the new one is returned
        result = self.navi_list_one_snap(format(self.snap_name))
        self.assertEquals(result.stdout, 'Name:  {0}'.format(self.snap_name))

if __name__ == '__main__':
    TestCase().run_test()
