package com.spglobal.rtservice;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.fanout.gripcontrol.GripControl;
import org.fanout.gripcontrol.GripPubControl;
import org.fanout.gripcontrol.WebSocketEvent;
import org.fanout.gripcontrol.WebSocketMessageFormat;
import org.fanout.pubcontrol.Format;
import org.fanout.pubcontrol.Item;
import org.fanout.pubcontrol.PublishFailedException;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import fi.iki.elonen.NanoHTTPD;

@SpringBootApplication
public class PushpinGWProxy extends NanoHTTPD implements InitializingBean {
	
	public PushpinGWProxy() throws IOException {
		super(8000);
		start(NanoHTTPD.SOCKET_READ_TIMEOUT, false);
		System.out.println("Server Started at Port:" + 8000);
	}

	@Autowired
	private SubscriptionHandlerforNode1 subscriptionHandler;

	@Autowired
	private TokenValidation tokenValidation;
	
	

	/*
	 * @Bean public SubscriptionHandlerforNode1 subscriptionHandler() {
	 * SubscriptionHandlerforNode1 st = new SubscriptionHandlerforNode1();
	 * System.out.println("Constructor Initialization==="+publisher_url);
	 * st.disconnectHanlder(); return st; }
	 */

	@Bean
	public WSO2ManagerService managerService() {
		return new WSO2ManagerService();
	}

	public static void main(String[] args) {

		SpringApplication.run(PushpinGWProxy.class, args);

	}

	// A helper class for publishing a message on a separate thread:
	private class PublishMessage implements Runnable {
		String channel;

		public PublishMessage(String channel) {
			this.channel = channel;
		}

		public void run() {

			Map<String, Object> entry = new HashMap<String, Object>();
			entry.put("control_uri", "http://localhost:5561");
			List<Map<String, Object>> config = Arrays.asList(entry);
			GripPubControl pub = new GripPubControl(config);
			List<String> channels = Arrays.asList(channel);
			List<Format> formats = Arrays
					.asList((Format) new WebSocketMessageFormat("Hello your channel Id:" + channel));
			try {
				pub.publish(channels, new Item(formats, null, null));
			} catch (PublishFailedException exception) {
				System.err.println("Publish failed: " + exception);
			}
		}
	}

	@Override
	public Response serve(IHTTPSession session) {

		// Validate the Grip-Sig header with a base64 encoded key: if
		/*
		 * if(!GripControl.validateSig(session.getHeaders().get("grip-sig"),
		 * "changeme")) return newFixedLengthResponse(Response.Status.UNAUTHORIZED,
		 * null, "invalid grip-sig token");
		 */
		// Only allow the POST method:
		Method method = session.getMethod();
		if (!Method.POST.equals(method))
			return newFixedLengthResponse(Response.Status.METHOD_NOT_ALLOWED, null, null);

		// Parse the request body:
		Map<String, String> body = new HashMap<String, String>();
		try {
			session.parseBody(body);
		} catch (IOException exception) {
			return newFixedLengthResponse(Response.Status.INTERNAL_ERROR, null, null);
		} catch (ResponseException exception) {
			return newFixedLengthResponse(Response.Status.INTERNAL_ERROR, null, null);
		}

		// Decode the WebSocket events.
		// Note: appending a new line is required because NanoHTTPD automatically
		// trims whitespace from the post data.
		System.out.println("============" + body.get("postData"));
		List<WebSocketEvent> inEvents = GripControl.decodeWebSocketEvents(body.get("postData") + "\r\n");

		Response response = connectHandler(session, inEvents);

		// Set the headers required by the GRIP proxy:
		response.addHeader("content-type", "application/websocket-events");
		response.addHeader("sec-websocket-extensions", "grip; message-prefix=\"\"");

		return response;
	}

	private Response connectHandler(IHTTPSession session, List<WebSocketEvent> inEvents) {
		Map<String, String> headersMap = session.getHeaders();

		/*
		 * String token = session.getCookies().read("SP_SSO_JWT_COOKIE"); if (token ==
		 * null) { token = session.getHeaders().get("authorization"); }
		 * 
		 * if (!tokenValidation.verifyTokenfromService(token)) { return
		 * newFixedLengthResponse(Response.Status.UNAUTHORIZED, null,
		 * "unauthorized request!"); }
		 */

		String responseBody = "";
		if (inEvents != null && inEvents.size() > 0 && inEvents.get(0).type.equals("OPEN")) {
			// create channel name based on connection
			String connectionId = headersMap.get("connection-id");
			String channelId = connectionId + "_channelid";
			channelId = "ch1";

			System.out.println("Channel Id:" + channelId);
			// Create channel hash map:
			Map<String, Object> channel = new HashMap<String, Object>();
			channel.put("channel", channelId);

			// Open the WebSocket and subscribe it to a channel:
			List<WebSocketEvent> outEvents = new ArrayList<WebSocketEvent>();
			outEvents.add(new WebSocketEvent("OPEN"));
			outEvents.add(new WebSocketEvent("TEXT", "c:" + GripControl.webSocketControlMessage("subscribe", channel)));
			responseBody = GripControl.encodeWebSocketEvents(outEvents);

			// Publish a message to the subscribed channel:
			new Thread(new PublishMessage(channelId)).start();
		}
		return newFixedLengthResponse(Response.Status.OK, null, responseBody);
	}

	private String onMessageHandler(IHTTPSession session, List<WebSocketEvent> inEvents) {
		// TO DO we need to handle the subscription message.
		return "";
	}

	private void disConnectHandler(IHTTPSession session, List<WebSocketEvent> inEvents) {
		// TO DO we need to handle the deletion of siddhi apps.

	}

	@Override
	public void afterPropertiesSet() throws Exception {
		subscriptionHandler.disconnectHanlder();
		
	}

}