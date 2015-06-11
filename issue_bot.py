#!/usr/bin/python

import os
import imaplib, email
import urllib2
import json


"""
Function Description : To read the configuration for email & github account, currently using simple file read operations
Input parameters : Filepath to read the configuration from
Return Value : Dictionary of configuration key, value pairs from ini file

"""
def read_config( filepath ):
	dict = {}
	if ( not os.path.exists( filepath ) or not os.path.isfile( filepath ) ):
		return {}
	with open( filepath ) as fh:
		for line in fh:
			( key, value ) = line.strip().split( '=' )
			dict[key] = value
	return dict


"""
Function Description : To parse the email body to get email details like Sender, Subject, Body 
Input parameters : Message body read from unread emails 
Return Value : Email Sender, Email Subject, Email Body

"""
def parse_email_body( msg ):
	emailBody = ""
	emailSubject = msg['Subject']
	emailFrom = msg['From']

	for part in msg.walk():
		if part.get_content_type() == "text/plain":
			body = part.get_payload( decode = True )
			emailBody =  body.decode( 'utf-8' )

	return emailFrom, emailSubject, emailBody


"""
Function Description : To get a list of unread emails for account mentioned in configuration 
Input parameters : Email Configuration details
Return Value : List of dictionary containing Email Sender, Email Subject, Email Body information if everything is successful or else empty list

"""
def get_unread_email_list( config ):
	emailList = []
	try:
		conn = imaplib.IMAP4_SSL( config['imap_server'] )
		conn.login( config['imap_username'], config['imap_password'] )
		conn.select( 'Inbox' )
		result, data = conn.search( None,'(UNSEEN)' )

		if ( result != 'OK' ):
			return []

		for num in data[0].split():
			result, data = conn.fetch( num, '(RFC822)' )
			sender, subject, body = parse_email_body( email.message_from_string( data[0][1] ) )
			emailList.append( {'from' : sender, 'subject' : subject, 'body' : body} )
			result, data = conn.store( num, '+FLAGS','\\Seen' )

		conn.close()
		return emailList

	except Exception, e:
		print "Exception Caught: %s" % str(e)
		return []


"""
Function Description : To create a GitHub issue for all the unread emails
Input parameters : Email dictionary & GitHub Configuration
Return Value : Nothing 

"""
def create_github_issue( emailList, config ):
	try:
		for email in emailList:
			params = {
				'title' : email['subject'],
				'body' : email['body']
			}
			head = { 'Authorization' : 'token %s' % config['token'] }
			conn = urllib2.Request( 'https://api.github.com/repos/%s/%s/issues' % ( config['username'], config['repo'] ), data = json.dumps(params), headers = head)
			urllib2.urlopen( conn )
	except Exception, e:
		print "Exception caught: %s" % str(e)


#Script starts Here

#Get the working directory
workDir = os.path.abspath( os.path.dirname( __file__ ) ) 


#Get the configuration parameters for GitHub account
gitConfig = read_config( '%s/github_config.ini' % workDir )


#Get the configuration parameters for Email account
emailConfig = read_config( '%s/email_config.ini' % workDir )


#Get the content of unread emails for configured account
emailList = get_unread_email_list( emailConfig )


#Create the GitHub issue in configured repository for above unread email list
create_github_issue( emailList, gitConfig )

#Script stops Here
