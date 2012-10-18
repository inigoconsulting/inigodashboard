from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC
from trac.test import EnvironmentStub, Mock, MockPerm
from trac.mimeview import Context
from trac.wiki.formatter import format_to_html
from trac.web.href import Href
from beaker.cache import cache_region

class MultiTracTicketManager(object):

    urls = {
        'clkss' : 'https://dev.inigo-tech.com/trac/clkss',
        'cis-india': 'https://dev.inigo-tech.com/trac/cis-india',
        'actalliance': 'https://dev.inigo-tech.com/trac/actalliance',
        'wcc': 'https://dev.inigo-tech.com/trac/wcc',
        'ilo.intranet': 'https://dev.inigo-tech.com/trac/ilo.intranet',
        'ilo.kn': 'https://dev.inigo-tech.com/trac/ilo.kn'
    }

    def __init__(self, username, password):

        self.username = username
        self.rpc = {}
        for name, url in self.urls.items():
            conf = TracConfig(url, username, password)
            self.rpc[name] = TracTicketXMLRPC(conf)

    def own_tickets(self):
        tickets = []
        for project, rpc in self.rpc.items():
            tickets += self._own_tickets_for_project(project)
        return sorted(tickets, key=lambda x: x['priority'])

    @cache_region('default_term')
    def _own_tickets_for_project(self, project):
        rpc = self.rpc[project]
        result = []
        for ticket in  rpc.query(owner=self.username):
            result.append(self._extract_ticketdata(project, ticket))
        return result

    def get_ticket(self, project, ticketid):
        rpc = self.rpc[project]
        ticket = rpc.get(ticketid)
        return self._extract_ticketdata(project, ticket)

    def _extract_ticketdata(self, project, ticket):
        data = {
            'project': project,
            'id': ticket.id,
            'url': ticket.url,
            'description-html': self._wiki_to_html(
                project,
                ticket.data['description']
            )
        }
        data.update(ticket.data)
        data['comments'] = []
        for comment in ticket.comments:
            data['comments'].append(
                self._extract_commentdata(project, comment)
            )
        return data

    def _extract_commentdata(self, project, comment):
        return {
            'author': comment.author,
            'time': comment.time,
            'comment': comment.comment,
            'comment-html': self._wiki_to_html(project, comment.comment)
        }

    def _wiki_to_html(self, project, wikitext):
        env = EnvironmentStub()
        req = Mock(href=Href(self.urls[project]), abs_href=Href(self.urls[project]),
                authname='anonymous', perm=MockPerm(), args={})
        context = Context.from_request(req, 'ticket')
        return format_to_html(env, context, wikitext)
