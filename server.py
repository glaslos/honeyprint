# Copyright (C) 2013  Lukas Rist <glaslos@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import logging
from pkipplib import pkipplib

from gevent.server import StreamServer

logger = logging.getLogger(__name__)


class PrintServer(object):

    def __init__(self):
        pass

    def handle(self, sock, address):
        print address
        data = sock.recv(8192)
        print repr(data)
        try:
            body = data.split('\r\n\r\n', 1)[1]
        except IndexError:
            body = data
        request = pkipplib.IPPRequest(body)
        request.parse()
        print request
        request = pkipplib.IPPRequest(operation_id=pkipplib.CUPS_GET_DEFAULT)
        request.operation["attributes-charset"] = ("charset", "utf-8")
        request.operation["attributes-natural-language"] = ("naturalLanguage", "en-us")
        sock.send(request.dump())

    def get_server(self, host, port):
        connection = (host, port)
        server = StreamServer(connection, self.handle)
        logger.info('LPR server started on: {0}'.format(connection))
        return server


if __name__ == "__main__":
    ps = PrintServer()
    print_server = ps.get_server("localhost", 9100)
    print_server.serve_forever()
