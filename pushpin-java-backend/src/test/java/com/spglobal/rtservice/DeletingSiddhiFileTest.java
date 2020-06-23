package com.spglobal.rtservice;

import static org.junit.Assert.*;

import java.io.File;
import java.io.IOException;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import com.spglobal.rtservice.WSO2ManagerService;

public class DeletingSiddhiFileTest {

	File rootpath = null;

	SubscriptionHandlerforNode1 managerService = null;
	
	@Rule
    public TemporaryFolder tempFolder = new TemporaryFolder();

	@Before
	public void before() throws IOException {
		rootpath = tempFolder.newFolder("siddhifiles");

		managerService = new SubscriptionHandlerforNode1();
	}

	@Test
	public void isDirectoryTest() {
		boolean isDir = rootpath.isDirectory();
		Assert.assertTrue(isDir);
	}
	
	@Test
    public void testCreateFile() throws IOException{
        File file = tempFolder.newFile("test.siddhi");
        assertTrue(file.exists());
    }
     

	@Ignore
	@Test
	public void deleteSiddhiAppsSucessTest() throws IOException {
		//File t=tempFolder.newFolder("siddhifiles");
		File t=tempFolder.newFile("test.siddhi");
		boolean isDeleted = managerService.deletingFilesRecursively(rootpath,"test.siddhi");
		Assert.assertTrue(isDeleted);

	}

	@Test
	public void deleteSiddhiAppsfailureTest() {
		boolean isDeleted = managerService.deletingFilesRecursively(rootpath, "ch1.siddhi");
		Assert.assertFalse(isDeleted);

	}
	

}
