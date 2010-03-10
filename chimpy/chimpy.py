import urllib
import urllib2
import pprint
import simplejson
from utils import transform_datetime
from utils import flatten
_debug = 1


class ChimpyException(Exception):
    pass


class Connection(object):
    """mailchimp api connection"""

    output = "json"
    version = '1.2'

    def __init__(self, apikey=None, secure=False, plugin_id=None):
        self._apikey = apikey
        self._plugin_id = plugin_id
        proto = 'http'
        if secure:
            proto = 'https'
        api_host = 'api.mailchimp.com'
        if '-' in apikey:
            key, dc = apikey.split('-')
        else:
            dc = 'us1'
        api_host = dc + '.' + api_host

        self.url = '%s://%s/%s/' % (proto, api_host, self.version)
        
    def _rpc(self, method, **params):
        """make an rpc call to the server"""

        params = urllib.urlencode(params, doseq=True)

        if _debug > 1:
            print __name__, "making request with parameters"
            pprint.pprint(params)
            print __name__, "encoded parameters:", params


        response = urllib2.urlopen("%s?method=%s" %(self.url, method), params)
        data = response.read()
        response.close()

        if _debug > 1:
            print __name__, "rpc call received", data

        result = simplejson.loads(data)

        try:
            if 'error' in result:
                raise ChimpyException(result['error'])
        except TypeError:
            # thrown when results is not iterable (eg bool)
            pass

        return result

    def _api_call(self, method, **params):
        """make an api call"""


        # flatten dict variables
        params = flatten(params)
        params['output'] = self.output
        params['apikey'] = self._apikey

        return self._rpc(method=method, **params)

    def ping(self):
        return self._api_call(method='ping')

    def lists(self):
        return self._api_call(method='lists')

    def list_batch_subscribe(self,
                             id,
                             batch,
                             double_optin=True,
                             update_existing=False,
                             replace_interests=False):

        return self._api_call(method='listBatchSubscribe',
                              id=id,
                              batch=batch,
                              double_optin=double_optin,
                              update_existing=update_existing,
                              replace_interests=replace_interests)

    def list_batch_unsubscribe(self,
                               id,
                               emails,
                               delete_member=False,
                               send_goodbye=True,
                               send_notify=False):

        return self._api_call(method='listBatchUnsubscribe',
                              id=id,
                              emails=emails,
                              delete_member=delete_member,
                              send_goodbye=send_goodbye,
                              send_notify=send_notify)

    def list_subscribe(self,
                       id,
                       email_address,
                       merge_vars,
                       email_type='text',
                        double_optin=True):
        return self._api_call(method='listSubscribe',
                              id=id,
                              email_address=email_address,
                              merge_vars=merge_vars,
                              email_type=email_type,
                              double_optin=double_optin)

    def list_unsubscribe(self,
                         id,
                         email_address,
                         delete_member=False,
                         send_goodbye=True,
                         send_notify=True):
        return self._api_call(method='listUnsubscribe',
                              id=id,
                              email_address=email_address,
                              delete_member=delete_member,
                              send_goodbye=send_goodbye,
                              send_notify=send_notify)

    def list_update_member(self,
                           id,
                           email_address,
                           merge_vars,
                           email_type='',
                           replace_interests=True):
        return self._api_call(method='listUpdateMember',
                              id=id,
                              email_address=email_address,
                              merge_vars=merge_vars,
                              email_type=email_type,
                              replace_interests=replace_interests)

    def list_member_info(self, id, email_address):
        return self._api_call(method='listMemberInfo',
                              id=id,
                              email_address=email_address)

    def list_members(self, id, status='subscribed'):
        return self._api_call(method='listMembers', id=id, status=status)

    def list_interest_groups(self, id):
        return self._api_call(method='listInterestGroups', id=id)

    def list_interest_group_add(self, id, name):
        return self._api_call(method='listInterestGroupAdd', id=id, group_name=name)

    def list_interest_group_del(self, id, name):
        return self._api_call(method='listInterestGroupDel', id=id, group_name=name)

    def list_merge_vars(self, id):
        return self._api_call(method='listMergeVars', id=id)

    def list_merge_var_add(self, id, tag, name, req=False):
        return self._api_call(method='listMergeVarAdd', id=id, tag=tag, name=name, req=req)

    def list_merge_var_del(self, id, tag):
        return self._api_call(method='listMergeVarDel', id=id, tag=tag)

    def campaign_abuse_reports(self, cid, **kwargs):
        """Get all email addresses that complained about a given campaign
        http://www.mailchimp.com/api/rtfm/campaignabusereports.func.php
        """
        return self._api_call(method='campaignAbuseReports', cid=cid, **kwargs)

    def campaign_content(self, cid):
        """Get the content (both html and text) for a campaign, exactly as it would appear in the campaign archive
        http://www.mailchimp.com/api/1.1/campaigncontent.func.php
        """

        return self._api_call(method='campaignContent', cid=cid)

    def campaign_create(self, campaign_type, options, content, **kwargs):
        """Create a new draft campaign to send.
        http://www.mailchimp.com/api/1.1/campaigncreate.func.php

        Optional parameters: segment_opts, type_opts
        """

        return self._api_call(method='campaignCreate', type=campaign_type, options=options, content=content, **kwargs)

    def campaign_delete(self, cid):
        """Delete a campaign.
        http://www.mailchimp.com/api/1.1/campaigndelete.func.php
        """

        return self._api_call(method='campaignDelete', cid=cid)

    def campaign_folders(self):
        """List all the folders for a user account.
        http://www.mailchimp.com/api/1.1/campaignfolders.func.php
        """

        return self._api_call(method='campaignFolders')

    def campaign_hard_bounces(self, cid, **kwargs):
        """Get all email addresses with Hard Bounces for a given campaign
        http://www.mailchimp.com/api/rtfm/campaignhardbounces.func.php
        """
        return self._api_call(method='campaignHardBounces', cid=cid, **kwargs)

    def campaign_pause(self, cid):
        """Pause a RSS campaign from sending.
        http://www.mailchimp.com/api/1.1/campaignpause.func.php
        """

        return self._api_call(method='campaignPause', cid=cid)

    def campaign_replicate(self, cid):
        """Replicate a campaign.
        http://www.mailchimp.com/api/1.1/campaignreplicate.func.php
        """

        return self._api_call(method='campaignReplicate', cid=cid)

    def campaign_resume(self, cid):
        """Resume sending a RSS campaign.
        http://www.mailchimp.com/api/1.1/campaignresume.func.php
        """

        return self._api_call(method='campaignResume', cid=cid)

    def campaign_schedule(self, cid, schedule_time, schedule_time_b=None):
        """Schedule a campaign to be sent in the future.
        http://www.mailchimp.com/api/1.1/campaignschedule.func.php
        """

        schedule_time = transform_datetime(schedule_time)

        if schedule_time_b:
            schedule_time_b = transform_datetime(schedule_time_b)

        return self._api_call(method='campaignSchedule', cid=cid, schedule_time=schedule_time, schedule_time_b=schedule_time_b)

    def campaign_send_now(self, cid):
        """Send a given campaign immediately.
        http://www.mailchimp.com/api/1.1/campaignsendnow.func.php
        """

        return self._api_call(method='campaignSendNow', cid=cid)

    def campaign_send_test(self, cid, test_emails, **kwargs):
        """Send a test of this campaign to the provided email address.
        Optional parameter: send_type
        http://www.mailchimp.com/api/1.1/campaignsendtest.func.php
        """

        if isinstance(test_emails, str):
            test_emails = [test_emails]

        return self._api_call(method='campaignSendTest', cid=cid, test_emails=test_emails, **kwargs)

    def campaign_soft_bounces(self, cid, **kwargs):
        """Get all email addresses with Soft Bounces for a given campaign
        http://www.mailchimp.com/api/rtfm/campaignsoftbounces.func.php
        """
        return self._api_call(method='campaignSoftBounces', cid=cid, **kwargs)

    def campaign_templates(self):
        """ Retrieve all templates defined for your user account """

        return self._api_call(method='campaignTemplates')

    def campaign_unschedule(self, cid):
        """Unschedule a campaign that is scheduled to be sent in the future  """

        return self._api_call(method='campaignUnschedule', cid=cid)

    def campaign_update(self, cid, name, value):
        """Update just about any setting for a campaign that has not been sent.
        http://www.mailchimp.com/api/1.1/campaignupdate.func.php
        """

        return self._api_call(method='campaignUpdate', cid=cid, name=name, value=value)

    def campaigns(self, filters={}, start=0, limit=50):
        """Get the list of campaigns and their details matching the specified filters.
        Timestamps should be passed as datatime objects.
        
        http://www.mailchimp.com/api/1.2/campaigns.func.php
        """
        
        return self._api_call(method='campaigns', filters=filters, start=start, limit=limit)

    def campaign_ecommerce_add_order(self,store_id,store_name,campaign_id,email_id,order):
        order['campaign_id'] = campaign_id
        order['email_id'] = email_id
        order['plugin_id'] = self._plugin_id
        order['store_id'] = store_id
        order['store_name'] = store_name
        order['campaign_id'] = campaign_id

        return self._api_call(method='campaignEcommAddOrder', order=order)

    def ecommerce_add_order(self,store_id,store_name,email,order,order_date):
        order['email'] = email
        order['plugin_id'] = self._plugin_id
        order['store_id'] = store_id
        order['store_name'] = store_name
        order['order_date'] = order_date

        return self._api_call(method='ecommAddOrder', order=order)

