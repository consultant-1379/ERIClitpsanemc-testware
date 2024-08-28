#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/Infra_tst_p_delete_snapshot

:Requirement   ID: OSS-70299
:TestCaseID:   infra_tst_p_delete_snapshot
:Title:        Delete a snapshot on the LUN using PSL
:Description:  Positive test case to delete a snapshot on the LUN using PSL
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Create a 1GB LUN on SAN
               2: Create two snapshots on the LUN, each with different name
               2.1: Verify the snapshots were created
               3: Delete one of the snapshots using
                  PSL delete_snapshot(<snap_name>)
               3.1: Verify the function returned True
               3.2: Verify the specified snapshot was deleted
               3.3: Verify the other snapshot still exists
               4: Using PSL, create a new snapshot with the same name as the
                  deleted one
               4.1: Verify the snapshot was created
               5: Delete the snapshots created during the test
               6: Delete the LUN created during the test
"""

#import unittest
from infra_utils.san_test import SanTest
from infra_utils.utils.san_utils import SanUtils


class TestCase(SanTest):

    """
    Test case to verify LUNs defined in the model
    """

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        self.sanapi_target = self.mws
        self.navi_target = self.mws

        # 1)
        # Create a 1GB LUN on SAN
        # This lun must not exist already in the SAN
        self.test_lun_name = ['vandals_test_delete_snapshot_lun_oss77090']
        self.create_luns_for_testing(self.test_lun_name)

        self.snap_names = ['snapshot_to_auto_test_snapshot_deletion',
                        'additional_snapshot_to_auto_test_snapshot_deletion']


    def tearDown(self):
        """
        Clean up after the test case
        """
        # Remove lun from Storage Group

        #5)
        # Delete the snapshots created during the test
        #6)
        # Delete the LUN created during the test
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Delete a snapshot on the LUN using PSL
            1. Create two snapshots of the test LUN, each with different name
            2. Delete the first snapshot
            3. Create a new snapshot with the same name as the deleted snapshot

        Actions:
            1: Assert that the output contains no errors
            2: Assert that the first snapshot was deleted
            3: Assert that a new snapshot could be created with the same name
        """

        # 2)
        # Create two snapshots on the LUN, each with different name
        for snap in self.snap_names:
            cmd = self.sanapi_create_snapshot(snap, self.test_lun_name[0])
            self.assertTrue(cmd.retcode == 0,
                            'Fail: create_snapshot failed')

        # 2.1) Verify the snapshots were created
        test_snapshot_dict = self.sanapi_get_snapshot(self.snap_names[0])
        sub_snapshot_dict = test_snapshot_dict[self.snap_names[0]]
        self.assertEqual(sub_snapshot_dict['snapshot name'],
                            self.snap_names[0],
                            "First snapshot created was not found")

        test_snapshot_dict_other = self.sanapi_get_snapshot(self.snap_names[1])
        sub_snapshot_dict_other = test_snapshot_dict_other[self.snap_names[1]]
        self.assertEqual(sub_snapshot_dict_other['snapshot name'],
                            self.snap_names[1],
                            "Second snapshot created was not found")

        # 3)
        # Delete one of the snapshots using PSL delete_snapshot(<snap_name>)
        # 3.1) Verify the function returned True
        cmd = self.sanapi_delete_snapshot(self.snap_names[0])
        self.assertTrue(cmd.retcode == 0,
                        'Fail: delete_snapshot() failed')


        #3.2) Verify the specified snapshot was deleted
        remaining_snapshot_dict =\
                    self.sanapi_list_snapshots_one_lun(self.test_lun_name[0])

        self.assertTrue(self.snap_names[0] not in remaining_snapshot_dict,
                    'Failure to delete test Snapshot \'{0}\''
                    .format(self.snap_names[0]))

        #3.3) Verify the other snapshot still exists
        self.assertTrue(self.snap_names[1] in remaining_snapshot_dict,
                    'Deletion of snapshot \'{0}\' occurred without permission'
                    .format(self.snap_names[1]))

        # 4)
        # Using PSL, create a new snapshot with the
        # same name as the deleted one
        create2 = self.sanapi_create_snapshot(self.snap_names[0],
                                              self.test_lun_name[0])
        self.assertTrue(create2.retcode == 0,
                        'Fail: create_snapshot failed')

        # 4.1) Verify the snapshot was created
        second_creation_snapshot_dict =\
                    self.sanapi_list_snapshots_one_lun(self.test_lun_name[0])

        self.assertTrue(self.snap_names[0] in second_creation_snapshot_dict,
                            "Recreated snapshot not found")

if __name__ == '__main__':
    TestCase().run_test()
