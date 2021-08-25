import logging

from flask import Flask, request, make_response

from telegram.client import get_all_sessions, manager_instance
from telegram.prober import send_message_and_wait_for_reply

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


def generate_metrics_response(success: bool, response_time: float) -> str:
    metrics = [
        '# HELP probe_success Displays whether or not the probe was a success',
        '# TYPE probe_success gauge',
        f'probe_success {1 if success else 0}',
    ]
    if success:
        metrics.extend([
            '# HELP probe_telegram_bot_response_time_seconds Returns the time taken for probe bot lookup in seconds',
            '# TYPE probe_telegram_bot_response_time_seconds gauge',
            f'probe_telegram_bot_response_time_seconds {response_time}',
        ])
    return '\n'.join(metrics)


@app.route('/probe')
async def telegram_bot_health_check():
    username = request.args.get('target')
    app.logger.info('checking %s', username)

    client = await manager_instance.get_next()
    duration = None
    try:
        result, duration = await send_message_and_wait_for_reply(client, username)
    except Exception as e:
        app.logger.error(e)
        result = False

    app.logger.info('result %s=%s', username, 'ok' if result else 'nok')
    response = make_response(generate_metrics_response(result, duration), 200 if result else 503)
    response.mimetype = "text/plain"
    return response


@app.route('/-')
def readiness_check():
    sessions = get_all_sessions()
    number_of_sessions = len(sessions)
    return make_response(f'number_of_sessions: {number_of_sessions}', 200 if number_of_sessions else 503)


if __name__ == '__main__':
    app.run()
