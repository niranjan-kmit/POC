package com.spglobal.rtservice;

import org.apache.http.client.methods.HttpPost;
import org.junit.Before;

public class TokenValidationTest {
	public static final String auth_url = "https://vpce-0a77c0e089b16b26e-mpbqp5to.execute-api.us-east-1.vpce.amazonaws.com/integ/token";

	HttpPost httpPost = null;

	@Before
	public void before() {
		httpPost = new HttpPost(auth_url);
		httpPost.addHeader("Authorization", "Basic Q0lRX1dFQjpQYXNzd29yZDEyMzQ=");
		httpPost.addHeader("x-apigw-api-id", "n8uhmtupi8");
		httpPost.addHeader("Content-Type", "application/x-www-form-urlencoded");
	}

}
