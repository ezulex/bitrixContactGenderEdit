import app_logger
from database_connection import check_name
from outgoing_webhooks import edit_contact_sex_by_id
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

logger = app_logger.get_logger(__name__)


class WebhookHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            event_type = data.get('event', '')

            if event_type == 'ONCRMCONTACTADD':
                contact_id = data.get('data').get('FIELDS').get('ID')
                contact_name = data.get('data').get('FIELDS').get('NAME')

                logger.info(f'Received webhook for new contact id={contact_id} with name "{contact_name}"')

                gender_from_db = check_name(contact_name)

                if gender_from_db == 1 or gender_from_db == 0:
                    if edit_contact_sex_by_id(contact_id, gender_from_db):
                        self._set_headers()
                        self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                    else:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(json.dumps({'status': 'internal error'}).encode('utf-8'))
                else:
                    self._set_headers()
                    self.wfile.write(
                        json.dumps({'status': f'name {contact_name} wasnt find in database'}).encode('utf-8'))
                    logger.warning(f'Name "{contact_name}" didnt exist in database')

            else:
                self.send_response(405)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'unsupported event'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=WebhookHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f'Starting server on port {port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Shutting down server')
        httpd.server_close()


if __name__ == '__main__':
    run()
