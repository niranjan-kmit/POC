package com.spglobal.rtservice;

import java.io.Serializable;
import java.util.Arrays;


public class Channel implements Serializable {

	
	private String channel;

	
	private String nodes[];
	


	public Channel() {
		super();
		// TODO Auto-generated constructor stub
	}
	
	public Channel(String channel, String[] nodes) {
		super();
		this.channel = channel;
		this.nodes = nodes;
	}

	public String getChannel() {
		return channel;
	}

	public void setChannel(String channel) {
		this.channel = channel;
	}

	public String[] getNodes() {
		return nodes;
	}

	public void setNodes(String[] nodes) {
		this.nodes = nodes;
	}

	@Override
	public String toString() {
		return "Channel [channel=" + channel + ", nodes=" + Arrays.toString(nodes) + "]";
	}

	
	

}
