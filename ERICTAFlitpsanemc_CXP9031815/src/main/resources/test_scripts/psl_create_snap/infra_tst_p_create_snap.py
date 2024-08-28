#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%2004

:Requirement   ID: OSS-77088
:TestCaseID:   infra_tst_p_create_snap.py
:Title:        Create snapshot of existing LUN with LUN name (using PSL)
:Description:  Positive test case to create snapshot of existing LUN
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist 
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Assert the output contains no errors
               2: Assert the snap shot was created with correct name
"""
from infra_utils.san_test import SanTest
from ptaf.utils.litp_cmd_utils import LitpUtils
from infra_utils.utils.san_utils import SanUtils

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
        self.snap_name="test_lun_oss77088_vandals1"
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
        Create snapshot of existing LUN
            1. Using sanapitest.py, create a snapshot of the test LUN
        Actions:
            1: Assert the output contains no errors
            2: Assert the snap shot was created with correct name
        """
        # Use NAVI command to verify the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

        # Create a snapshot of the test lun (PSL)
        cmd = self.sanapi_create_snapshot(self.snap_name, \
                                          self.test_lun_names[0])
        self.assertTrue(cmd.retcode == 0)

        # Use NAVI command to verify that the snapshot exists
        list = self.navi_list_one_snap(self.snap_name)

        # Verify the log output
        snapshot_metadict = SanUtils.get_snapshotinfo_from_stdout(cmd.stdout)
        snapshot_subdict = snapshot_metadict[self.snap_name]
        
        self.assertTrue(self.snap_name in snapshot_metadict)
        self.assertEqual(snapshot_subdict['snapshot name'], self.snap_name)
        self.assertEqual(snapshot_subdict['resource lun name'], \
                         self.test_lun_names[0])

if __name__ == '__main__':
    TestCase().run_test()
