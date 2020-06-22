package com.spglobal.rtservice;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.springframework.stereotype.Service;

@Service
public class TokenValidation {
	
	public static final String auth_url = "https://vpce-0a77c0e089b16b26e-mpbqp5to.execute-api.us-east-1.vpce.amazonaws.com/integ/token";
	
	public  boolean verifyTokenfromService(String token) {
		HttpPost httpPost = new HttpPost(auth_url);

		httpPost.addHeader("Authorization", "Basic Q0lRX1dFQjpQYXNzd29yZDEyMzQ=");
		httpPost.addHeader("x-apigw-api-id", "n8uhmtupi8");
		httpPost.addHeader("Content-Type", "application/x-www-form-urlencoded");

		String body = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&scope=UserProfile.me&assertion="
				+ token;
		try {
			httpPost.setEntity(new StringEntity(body));
			try (CloseableHttpClient httpClient = HttpClients.createDefault();
					CloseableHttpResponse response = httpClient.execute(httpPost)) {

				return response.getStatusLine().getStatusCode()==200;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		return false;
	}

}
