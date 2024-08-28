package com.ericsson.nms.litp.taf.test_cases;

/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2015
 *
 * The copyright to the computer program(s) herein is the property of
 * Ericsson Inc. The programs may be used and/or copied only with written
 * permission from Ericsson Inc. or in accordance with the terms and
 * conditions stipulated in the agreement/contract under which the
 * program(s) have been supplied.
 *******************************************************************************
 *----------------------------------------------------------------------------*/

import org.testng.annotations.*;
import utils.PtafTestRunner;
import com.ericsson.cifwk.taf.*;
import com.ericsson.cifwk.taf.annotations.*;


public class TestRunner3 extends PtafTestRunner implements TestCase {

	// Location of the python test scripts
	private String scriptsDirectory = "psl_restore_snap";

	// Specify the csv data file to use
	// test_id represents the script name and vargs any arguments you wish to
	// pass
	@DataDriven(name = "restore_snapshots_test_scripts")
	@Test
	@Context(context = { Context.CLI })
	public void execute_python_script(@TestId @Input("test_id") String test_id,
			@Input("vargs") String vargs) {
		executePythonScript(scriptsDirectory, test_id, vargs);
	}

}
