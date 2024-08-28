#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/8882

:Requirement   ID: OSS-84540
:TestCaseID:   infra_tst_p_expand_lun
:Title:        Expand a storage pool LUN using the PSL
:Description:  Positive test case to expand a pool LUN using PSL
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Create a 1GB LUN on SAN
               2: Using the PSL expand the LUN to 5GB
               3: Verify the LUn was expanded to 5GB
               4: Delete the expanded LUN
"""
from infra_utils.san_test import SanTest
from infra_utils.utils.san_utils import SanClient


class TestCase(SanTest):
    """
    Test case to verify LUN expansion
    """
    
    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        self.navi_target = self.mws
        self.san_client = SanClient(self.san, navi_target=self.navi_target)

        # 1)
        # Create a 1GB LUN on SAN
        # This lun must not exist already in the SAN
        self.test_lun_name = ['infra_p_expand__lun_oss84540']
        self.create_luns_for_testing(self.test_lun_name)

    def tearDown(self):
        """
        Clean up after the test case
        """
        # 4)
        # Delete the LUN created during the test
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Expand a pool LUN using the PSL
            1. Expand the LUN created earlier to 5GB

        Actions:
            1: Assert that the output contains no errors
            2: Assert the size of the LUN is 5GB
        """
        # 2)
        # Using the PSL expand the LUN to 5GB
        cmd = self.san_client.sanapi_expand_pool_lun(self.test_lun_name[0], lun_size="5gb")
        self.assertTrue(cmd.retcode == 0)

        # 3.)
        # Verify the LUN was expanded to 5gb
        test_lun = self.san_client.navi_get_lun(self.test_lun_name[0])
        test_lun_size = test_lun['User Capacity (GBs)']
        self.assertEquals(self.test_lun_name[0], test_lun['Name'])
        self.assertEquals("5.000", test_lun_size)

if __name__ == '__main__':
    TestCase().run_test()
