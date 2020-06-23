package com.spglobal.rtservice;

import java.io.File;
import java.sql.Array;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Arrays;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.zeromq.SocketType;
import org.zeromq.ZContext;
import org.zeromq.ZMQ;

@Configuration
@Component
public class SubscriptionHandlerforNode1 extends ZContext {

	static Logger logger = LoggerFactory.getLogger(SubscriptionHandlerforNode1.class);

	@Value("${pushpin.databasename}")
	private String databaseName;

	@Value("${pushpin.table}")
	private String table;

	@Value("${pushpin.host_url}")
	private String host;

	@Value("${pushpin.database.user}")
	private String user;
	
	@Value("${pushpin.database.password}")
	private String password;
	
	

	public static final String PUSHPIN_NODE = "NODE1";

	String rootPath = "/siddhi-files/";
	File dirFile = new File(rootPath);

	public SubscriptionHandlerforNode1() {
	}

	@Bean
	public WSO2ManagerService managerService() {
		return new WSO2ManagerService();
	}

	public void disconnectHanlder() {
		ZContext context = null;
		Connection connection = null;
		try {
			context = new ZContext();
			// Socket to talk to clients
			ZMQ.Socket socket = context.createSocket(SocketType.XPUB);
			socket.setRcvHWM(0);
			socket.setImmediate(true);
			socket.connect("tcp://localhost:5562");

			connection = DriverManager.getConnection(host,user,password);

			Statement statement = connection.createStatement();

			byte[] srr = socket.recv();
			int type = (int) srr[0];
			byte[] topic = Arrays.copyOfRange(srr, 1, srr.length);
			String topicName = new String(topic);

			if (0 == type) {

				if (validateWithAllNodes(topicName)) {
					String t = "SELECT * FROM pushpin_subscription WHERE channel='" + topicName + "'";
					ResultSet resultSet = statement.executeQuery(t);
					boolean isresult = resultSet.next();
					if (isresult) {
						Array nodesArr = resultSet.getArray("nodes");
						String[] nodes = (String[]) nodesArr.getArray();
						String qpreparation = "";
						for (int k = 0; k < nodes.length; k++) {
							if (!PUSHPIN_NODE.equals(nodes[k])) {
								qpreparation = qpreparation + "\"" + nodes[k] + "\"" + ",";
							}
						}
						qpreparation = qpreparation.substring(0, qpreparation.length() - 1);
						updateQuery(statement, topicName, nodes, qpreparation);
					}

				} else {
					deleteSiddhiApp(statement, topicName);
				}

			} else {
				try {
					String t = "SELECT * FROM pushpin_subscription WHERE channel='" + topicName + "'";
					ResultSet resultSet = statement.executeQuery(t);
					boolean isresult = resultSet.next();
					if (isresult) {
						Array nodesArr = resultSet.getArray("nodes");
						String[] nodes = (String[]) nodesArr.getArray();
						String qpreparation = "";
						for (int k = 0; k < nodes.length; k++) {
							qpreparation = qpreparation + "\"" + nodes[k] + "\"" + ",";
						}
						qpreparation = qpreparation + "\"" + PUSHPIN_NODE + "\"";
						updateQuery(statement, topicName, nodes, qpreparation);
					} else {
						createQuery(statement, topicName);
					}

				} catch (SQLException e) {
					logger.debug("connection failure");
					e.printStackTrace();
				}
				logger.info("subscription topic name:=>" + topicName);
			}

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			context.close();
			// connection.close();
		}
	}

	private void deleteSiddhiApp(Statement statement, String topicName) throws SQLException {
		boolean isDeleted = statement.execute("DELETE FROM pushpin_subscription WHERE channel='" + topicName + "'");
		if (isDeleted) {
			deletingFilesRecursively(dirFile, topicName + ".siddhi");
		}
		logger.info("deleted the channel with name:" + topicName);
	}

	private void updateQuery(Statement statement, String topicName, String[] nodes, String qpreparation)
			throws SQLException {
		String query = "UPDATE pushpin_subscription SET nodes=" + "'" + "{" + qpreparation + "}" + "'"
				+ " WHERE channel=" + "'" + topicName + "'";
		System.out.println("=========>" + query);
		boolean isSaved = statement.execute(query);
		if (isSaved) {
			logger.info("new node assigned to channel:" + nodes);
		}
	}

	private void createQuery(Statement statement, String topicName) throws SQLException {
		String eQuery = "'" + topicName + "'" + "," + "'" + "{" + "\"" + PUSHPIN_NODE + "\"" + "}" + "'";
		String query = "INSERT INTO pushpin_subscription(channel,nodes) values(" + eQuery + ")";
		System.out.println("=========>" + query);
		boolean isSaved = statement.execute(query);
		if (isSaved) {
			logger.info("new node assigned to channel:" + PUSHPIN_NODE);
		}
	}

	public boolean deletingFilesRecursively(File rootPath, String file) {
		// file = file + ".siddhi";
		for (File subFile : rootPath.listFiles()) {
			if (subFile.isDirectory()) {
				deletingFilesRecursively(subFile, file);
			} else if (subFile.isFile() && subFile.getName().equals(file)) {
				System.out.println("file name :" + file + "was removed.");
				return subFile.delete();

			}
		}
		return false;

	}

	private boolean validateWithAllNodes(String topicName) {
		try {
			Connection connection = DriverManager.getConnection(host,user,password);
			System.out.println("Connected to PostgreSQL database!");
			Statement statement = connection.createStatement();
			ResultSet resultSet = statement
					.executeQuery("SELECT * FROM realtime.pushpin_subscription WHERE channel='" + topicName + "'");
			while (resultSet.next()) {
				System.out.printf("deleted channel" + resultSet.getString("channel"));
				Array nodesArr = resultSet.getArray("nodes");
				String[] nodes = (String[]) nodesArr.getArray();
				// System.out.printf("%-30.30s", nodes);
				return nodes.length > 1;

			}

		} catch (SQLException e) {
			System.out.println("Connection failure.");
			e.printStackTrace();
		}
		return false;
	}

}
