package com.spglobal.rtservice;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@ConfigurationProperties("spring.datasource")
public class PushpinConfiguration {
	
	@Profile("dev")
	@Bean
	public String devConfiguration() {
		System.out.println("Dev Configuration");
		return "Dev Propertiese Configured";
	}
	
	@Profile("sandbox")
	@Bean
	public String sandBoxConfiguration() {
		System.out.println("sandbox Configuration");
		return "Sandbox Propertiese Configured";
	}

}
