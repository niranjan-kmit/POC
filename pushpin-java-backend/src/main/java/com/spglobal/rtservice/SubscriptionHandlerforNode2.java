package com.spglobal.rtservice;

import java.io.File;
import java.util.Arrays;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.zeromq.SocketType;
import org.zeromq.ZContext;
import org.zeromq.ZMQ;

@Configuration
@Component
public class SubscriptionHandlerforNode2 extends ZContext {
	
	@Value("${publisher_url}")
	private String publisher_url;
	
	private WSO2ManagerService managerService;
	
	String rootPath = "/siddhi-files/";
	File dirFile = new File(rootPath);
	
	public SubscriptionHandlerforNode2() {
		//disconnectHanlder();
		managerService=new WSO2ManagerService();
	}
	
	@Bean
	public WSO2ManagerService managerService() {
		return new WSO2ManagerService();
	}

	public void disconnectHanlder() {
		try (ZContext context = new ZContext()) {
			// Socket to talk to clients
			ZMQ.Socket socket = context.createSocket(SocketType.XPUB);
			socket.setRcvHWM(0);
			socket.setImmediate(true);
			socket.connect("tcp://localhost:5562");

			while (true) {
                
				byte[] srr = socket.recv();
				int type = (int) srr[0];
				byte[] topic = Arrays.copyOfRange(srr, 1, srr.length);
				String topicName = new String(topic);

				if (0 == type) {
					managerService.deletingFilesRecursively(dirFile, topicName);
					System.out.println(publisher_url+" UNSUB=====>" + topicName);
				} else {
					System.out.println("  SUB=====>" + topicName);
				}
				

			}
		}
	}
}
