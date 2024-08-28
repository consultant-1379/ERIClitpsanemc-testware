#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%2005

:Requirement   ID: OSS-77088
:TestCaseID:   infra_tst_p_create_second_snap_on_lun.py
:Title:        Create a snapshot of a LUN which already has a snap-shot
:Description:  Positive test case to create a snapshot of a LUN which already 
               has a snap-shot
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist 
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Assert the output contains no errors
               2: Assert the snap shot was created with correct name
"""

from infra_utils.san_test import SanTest
from ptaf.utils.litp_cmd_utils import LitpUtils
from infra_utils.utils.san_utils import SanUtils
import cmd

class TestCase(SanTest):
    
    def setUp(self):
        """
        Setup the test
        """
        super(TestCase, self).setUp()
        self.litp_utils = LitpUtils()
        self.sanapi_target = self.mws
        self.navi_target = self.mws
        
        # Create test lun. This lun must not exist already in the SAN
        self.snap_names = ["v1","v2"]
        self.test_lun_names = ['test_lun_oss77088']
        self.create_luns_for_testing(self.test_lun_names)

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Create a snapshot of a LUN which already has a snap-shot
            1. Create a snap shot then create a second snap shot
        Actions:
            1: Assert the output contains no errors
        """

        # Use NAVI command to verify that the snapshots do not exist
        for snaps in self.snap_names:
            list = self.navi_list_one_snap(snaps)
            self.assertTrue(list.retcode == 1)

        # Create snapshot of the test lun (PSL)
        for testlun in self.test_lun_names:
            for snap in self.snap_names:
                snap = testlun + '_' + snap
                cmd = self.sanapi_create_snapshot(snap, testlun)
    
                # Verify the log output
                snapshot_metadict = SanUtils.get_snapshotinfo_from_stdout(\
                                                                    cmd.stdout)
                snapshot_subdict = snapshot_metadict[snap]
                
                self.assertTrue(cmd.retcode == 0)               
                self.assertTrue(snap in snapshot_metadict)               
                self.assertEqual(snapshot_subdict['snapshot name'], snap)
                self.assertEqual(snapshot_subdict['resource lun name'],testlun)

        # Use NAVI command to verify that the snapshots exists
        for snaps in self.snap_names:
            list = self.navi_list_one_snap(snaps)
            self.assertTrue(list.retcode == 0)

if __name__ == '__main__':
    TestCase().run_test()
