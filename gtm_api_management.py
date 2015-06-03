# Note: This code assumes you have an authorized tagmanager service object.

import sys
import argparse
import xlwt


from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


"""Access and manage a Google Tag Manager account."""

import argparse
import sys

import httplib2

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


def GetService(api_name, api_version, scope, client_secrets_path):
  """Get a service that communicates to a Google API.

  Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    scope: A list of strings representing the auth scopes to authorize for the
      connection.
    client_secrets_path: string A path to a valid client secrets file.

  Returns:
    A service that is connected to the specified API.
  """
  # Parser command-line arguments.
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])

  # Set up a Flow object to be used if we need to authenticate.
  flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))

  # Prepare credentials, and authorize HTTP object with them.
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to a file.
  storage = file.Storage(api_name + '.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def main(argv):
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/tagmanager.readonly']

  # Authenticate and construct service.
  service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')

  # This request lists all container versions for the authorized user.
  try:
       versions = service.accounts().containers().versions().list(
            accountId='20203224', containerId='761067').execute()
       print_versions(versions)
  except TypeError, error:
       # Handle errors in constructing a query.
       print 'There was an error in constructing your query : %s' % error
  except HttpError, error:
       # Handle API errors.
       print ('There was an API error : %s : %s' %
              (error.resp.status, error.resp.reason))


def print_versions(versions):
# The results of the list method are stored in the versions object.
# The following code shows how to iterate through them.

     for version in versions.get('containerVersion', []):   
       print 'Container Version'
       print 'Account Id = %s' % version.get('accountId')
       print 'Container Id = %s' % version.get('containerId')
       print 'Container Version Id = %s' % version.get('containerVersionId')
       print 'Version Name = %s' % version.get('name')
       print 'Version Deleted = %s' % version.get('deleted')
       print 'Version Notes = %s' % version.get('notes')
       print 'Version Fingerprint = %s\n\n' % version.get('fingerprint')

       # Get the container object.
       container = version.get('container', {})
       print 'Container Name = %s' % container.get('name')
       for domain in container.get('domainName', []):
         print 'Domain Name = %s' % domain
         print 'Timezone Country Id = %s' % container.get('timeZoneCountryId')
         print 'Timezone Id = %s' % container.get('timeZone')
         print 'Notes = %s' % container.get('notes')
         for usageContext in container.get('usageContext'):
              print 'Usage Context = %s' % usageContext
         print 'Container Fingerprint = %s\n\n' % container.get('fingerprint')

       # Get the macro objects.
       for macro in version.get('macro', []):
         print 'Macro Id = %s' % macro.get('macroId')
         print 'Macro Name = %s' % macro.get('name')
         print 'Macro Type = %s' % macro.get('type')
         print 'Macro notes = %s' % macro.get('notes')
         print 'Schedule Start ms = %s' % macro.get('scheduleStartMs')
         print 'Schedule End ms = %s' % macro.get('scheduleEndMs')
         for parameter in macro.get('parameter', []):
           print 'Parameter Type = %s' % parameter.get('type')
           print 'Parameter Key = %s' % parameter.get('key')
           print 'Parameter Value = %s' % parameter.get('value')
         for enablingRuleId in macro.get('enablingRuleId', []):
           print 'Macro Enabling Rule Id = %s' % enablingRuleId
         for disablingRuleId in macro.get('disablingRuleId', []):
           print 'Macro Disabling Rule Id = %s' % disablingRuleId
         print 'Macro Fingerprint = %s\n\n' % macro.get('fingerprint')

       # Get the rule object.
       for rule in version.get('rule'):
         print 'Rule Id = %s' % rule.get('ruleId')
         print 'Rule Name = %s' % rule.get('name')
         print 'Rule Notes = %s' % rule.get('notes')
         for condition in rule.get('condition', []):
           print 'Condition Type = %s' % condition.get('type')
           for parameter in condition.get('parameter', []):
             print 'Condition Parameter Type = %s' % condition.get('type')
             print 'Condition Parameter Key = %s' % condition.get('key')
             print 'Condition Parameter Value = %s' % condition.get('value')
         print 'Rule Fingerprint = %s\n\n' % rule.get('fingerprint')

       # Get the tag objects.
       for tag in version.get('tag', []):
         print 'Tag Id = %s' % tag.get('tagId')
         print 'Tag Name = %s' % tag.get('name')
         print 'Tag Type = %s' % tag.get('type')
         for firingRuleId in tag.get('firingRuleId', []):
           print 'Tag Firing Rule Id = %s' % firingRuleId
         for blockingRuleId in tag.get('blockingRuleId', []):
           print 'Tag Blocking Rule Id = %s' % blockingRuleId
         print 'Tag Live Only = %s' % tag.get('liveOnly')

         # Get tag priority.
         priority = tag.get('priority', {})
         print 'Tag Priority Type = %s' % priority.get('type')
         print 'Tag Priority Key = %s' % priority.get('key')
         print 'Tag Priority value = %s' % priority.get('value')

         # Get tag dependencies.
         dependencies = tag.get('dependencies', {})
         print 'printing Dependencies: %s' % dependencies
         print 'Dependencies Type = %s' % dependencies.get('type')
         print 'Dependencies Key = %s' % dependencies.get('key')
         print 'Dependencies Value = %s' % dependencies.get('value')

         print 'Tag Notes = %s' % tag.get('notes')
         print 'Tag Schedule Start ms = %s' % tag.get('scheduleStartMs')
         print 'Tag Schedule End ms = %s' % tag.get('scheduleEndMs')
         for parameter in tag.get('parameter', []):
           print 'Parameter Type = %s' % parameter.get('type')
           print 'Parameter Key = %s' % parameter.get('key')
           print 'Parameter Value = %s' % parameter.get('value')
         print 'Tag Fingerprint = %s\n\n' % tag.get('fingerprint')

if __name__ == '__main__':
  main(sys.argv)

