import app_logger
from database_connection import check_name
from outgoing_webhooks import edit_contact_sex_by_id, get_contact_name_by_id
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

logger = app_logger.get_logger(__name__)


class WebhookHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        try:
            if self.path == '/webhook':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                logger.info(post_data)

                try:
                    data = json.loads(post_data)
                except json.decoder.JSONDecodeError as e:
                    logger.error(f'Error decoding JSON: {e}')
                    self.send_response(400)
                    self.end_headers()
                    return

                event_type = data.get('event', '')

                if event_type == 'ONCRMCONTACTADD':
                    contact_data = data.get('data', {}).get('FIELDS', {})
                    contact_id = contact_data.get('ID')
                    # contact_name = contact_data.get('NAME')
                    contact_name = get_contact_name_by_id(contact_id)

                    logger.info(f'Received webhook for new contact id={contact_id} with name "{contact_name}"')

                    gender_from_db = check_name(contact_name)

                    if gender_from_db in [0, 1]:
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
                            json.dumps({'status': f'name {contact_name} wasnt found in database'}).encode('utf-8'))
                        logger.warning(f'Name "{contact_name}" not found in database')

                else:
                    self.send_response(405)
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'unsupported event'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f'Error processing request: {e}')
            self.send_response(500)
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
