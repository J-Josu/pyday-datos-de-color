#!/usr/bin/env python3

import shlex
import subprocess
import os
import argparse
import platform


DEV_DEPENDENCIES = 'pytailwindcss websockets python-dotenv'

DEFAULT_STATIC_FOLDER = 'static'
DEFAULT_TEMPLATE_FOLDER = 'src/web/templates'
DEFAULT_TEMPLATE_GLOB = '**/*.html'
DEFAULT_TEMPLATE_ROOT_LAYOUT = 'layout.html'
DEFAULT_LIVE_RELOAD_FILE = 'dev/live_reload.js'
DEFAULT_GENERATED_CSS_FILE = 'dev/tailwindcss.css'
DEFAULT_MINIFIED_CSS_FILE = 'tailwindcss_min.css'


def generate_tw_config(content_glob: str) -> str:
    return ('''
// Docs: https://tailwindcss.com/docs/configuration

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "''' + content_glob + '''"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
''').lstrip()


def generate_live_reload_template(css_file: str, js_file: str, minified_css_file: str) -> str:
    return ('''
{% if config.DEBUG %}
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename=\'''' + css_file + '''\') }}">
  <script src="{{ url_for('static', filename=\'''' + js_file + '''\') }}" defer></script>
{% else %}
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename=\'''' + minified_css_file + '''\') }}">
{% endif %}
''').strip()


def generate_layout_template(css_file: str, js_file: str, minified_css_file: str) -> str:
    return ('''
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}{% endblock %}</title>
  ''' + generate_live_reload_template(css_file, js_file, minified_css_file) + '''
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
''').lstrip()


class Term:
    if platform.system() == 'Windows':
        os.system('color')

    BLACK = "\033[30m"
    R = "\033[31m"
    G = "\033[32m"
    BG = "\033[1;32m"
    Y = "\033[33m"
    B = "\033[34m"
    M = "\033[35m"
    C = "\033[36m"
    W = "\033[37m"
    ENDC = "\033[0;0m"
    NORMAL = "\033[1m"
    BOLD = "\033[1m"

    @staticmethod
    def dev(*values: object, end: str = '\n', sep: str = ' '):
        print(f'{Term.M}[dev]{Term.ENDC}', *values, end=end, sep=sep)

    @staticmethod
    def info(*values: object, end: str = '\n', sep: str = ' '):
        print(f'{Term.C}[info]{Term.ENDC}', *values, end=end, sep=sep)

    @staticmethod
    def warn(*values: object, end: str = '\n', sep: str = ' '):
        print(f'{Term.Y}[warn]{Term.ENDC}', *values, end=end, sep=sep)

    @staticmethod
    def error(*values: object, end: str = '\n', sep: str = ' '):
        print(f'{Term.R}[error]{Term.ENDC}', *values, end=end, sep=sep)

    @staticmethod
    def confirm(message: str) -> bool:
        response = input(
            f'{Term.C}{message}{Term.ENDC} [y/N] ').strip().lower()
        while True:
            if not response or response.startswith('n'):
                return False
            if response.startswith('y'):
                return True
            print(f'{Term.R}Invalid response{Term.ENDC}')
            response = input(
                f'{Term.C}{message}{Term.ENDC} [y/N] ').strip().lower()

    @staticmethod
    def ask_fs_entry(message: str, entry_type: str = 'file'):
        if entry_type not in ('file', 'dir'):
            raise ValueError(f'Invalid entry type: {entry_type}')

        response = input(f'{Term.C}{message}{Term.ENDC} ').strip()

        while True:
            if not response:
                print(f'{Term.R}Invalid response{Term.ENDC}')
                response = input(f'{Term.C}{message}{Term.ENDC} ').strip()
                continue

            if entry_type == 'file':
                if os.path.isfile(response):
                    return response
                print(f'{Term.R}File not found{Term.ENDC}')
                response = input(f'{Term.C}{message}{Term.ENDC} ').strip()
                continue

            if os.path.isdir(response):
                return response
            print(f'{Term.R}Directory not found{Term.ENDC}')
            response = input(f'{Term.C}{message}{Term.ENDC} ').strip()


def check_installation_requirements():
    cwd = os.getcwd()
    Term.warn(
        f'The installation will continue on the current working directory:\n> {Term.BOLD}{cwd}{Term.ENDC} ')
    continue_install = Term.confirm("Continue?")

    if not continue_install:
        Term.dev("Installation canceled")
        return 1

    python_cmd = shlex.split("python --version")
    python_cmd_result = subprocess.run(
        python_cmd, shell=True, check=True, capture_output=True
    )

    if python_cmd_result.returncode != 0:
        Term.error('python --version failed, terminating script')
        return python_cmd_result.returncode

    version = python_cmd_result.stdout.decode('utf-8')
    if version != 'Python 3.8.10':
        Term.warn("Current python version is 3.8.10")
        continue_install = Term.confirm("Continue?")
        if not continue_install:
            Term.dev("Installation canceled")
            return 1

    return 0


def install_dev_dependencies():
    poetry_cmd = shlex.split(f"poetry add --group=dev {DEV_DEPENDENCIES}")

    try:
        subprocess.run(poetry_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        Term.error(e)
        Term.error('Dev dependencies installation failed, terminating script')
        exit(1)


def init_tailwindcss(content_glob: str):
    tailwind_init = "tailwindcss init"

    try:
        subprocess.run(tailwind_init, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        Term.error(e)
        Term.error('Tailwindcss initialization failed, terminating script')
        exit(1)

    with open('tailwind.config.js', 'w') as f:
        f.write(generate_tw_config(content_glob))


def generate_files(static_folder: str, live_reload_file: str, generated_css_file: str, minified_css_file: str):
    with open('dev.py', 'w') as f:
        f.write(generate_dev_script(static_folder,
                generated_css_file, minified_css_file))

    live_reload_js_path = f'{static_folder}/{live_reload_file}'
    try:
        with open(live_reload_js_path, 'w') as f:
            f.write(JAVASCRIPT_LIVE_RELOAD_SCRIPT)
    except FileNotFoundError:
        os.makedirs(
            os.path.dirname(live_reload_js_path),
            exist_ok=True
        )
        with open(live_reload_js_path, 'w') as f:
            f.write(JAVASCRIPT_LIVE_RELOAD_SCRIPT)


def update_layout(templates_folder: str, template_root_layout: str, static_folder: str, live_reload_file: str, generated_css_file: str, minified_css_file: str):
    root_layout = f'{templates_folder}/{template_root_layout}'

    try:
        with open(root_layout, '+r') as f:
            layout = f.read()
            if '</head>' not in layout:
                print("Error: </head> tag not found in src/web/templates/layout.html")
                exit(1)
            layout = layout.replace(
                '</head>',
                generate_live_reload_template(
                    generated_css_file,
                    live_reload_file,
                    minified_css_file
                ) + '</head>'
            )
            f.seek(0)
            f.write(layout)
            f.truncate()
    except FileNotFoundError as e:
        Term.warn(e)
        os.makedirs(
            os.path.dirname(root_layout),
            exist_ok=True
        )
        with open(root_layout, 'w') as f:
            f.write(generate_layout_template(
                generated_css_file,
                live_reload_file,
                minified_css_file
            ))


def update_gitignore(static_folder: str, live_reload_file: str, generated_css_file: str):
    content = f'''
# dev mode
dev.py
{static_folder}/{live_reload_file}
{static_folder}/{generated_css_file}
'''

    try:
        with open('.gitignore', 'a') as f:
            f.write(content)
    except FileNotFoundError as e:
        Term.warn(e)
        with open('.gitignore', 'w') as f:
            f.write(content)


def self_clean():
    os.remove(os.path.realpath(__file__))


def main() -> None:
    cli_args = cli().parse_args()

    Term.dev('Starting installation...')

    check_code = check_installation_requirements()
    if check_code != 0:
        exit(check_code)

    install_dev_dependencies()

    content_glob = f'{cli_args.templates_folder}/{cli_args.templates_glob}'
    init_tailwindcss(content_glob)

    generate_files(
        cli_args.static_folder,
        cli_args.live_reload_file,
        cli_args.generated_css_file,
        cli_args.minified_css_file
    )

    update_layout(
        cli_args.templates_folder,
        cli_args.template_root_layout,
        cli_args.static_folder,
        cli_args.live_reload_file,
        cli_args.generated_css_file,
        cli_args.minified_css_file
    )

    if cli_args.gitignore:
        update_gitignore(
            cli_args.static_folder,
            cli_args.live_reload_file,
            cli_args.generated_css_file
        )

    if cli_args.clean:
        self_clean()
        Term.dev('Cleaned installation script')

    Term.dev('Installation complete :)')
    exit(0)


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Install dev mode for the project.',
        allow_abbrev=True
    )

    parser.add_argument(
        '-c', '--clean', dest='clean', action='store_true', default=False,
        help='Clean the installation script after execution. Default: False'
    )

    parser.add_argument(
        '-gi', '--gitignore', dest='gitignore', action='store_true', default=False,
        help='Update .gitignore to exclude dev mode related files. Default: False'
    )

    parser.add_argument(
        '-s', '--static-folder', dest='static_folder', type=str, default=DEFAULT_STATIC_FOLDER,
        help=f'Static folder path. Default: {DEFAULT_STATIC_FOLDER}'
    )

    parser.add_argument(
        '-tf', '--templates-folder', dest='templates_folder', type=str, default=DEFAULT_TEMPLATE_FOLDER,
        help=f'Templates folder path. Default: {DEFAULT_TEMPLATE_FOLDER}'
    )
    parser.add_argument(
        '-tg', '--templates-glob', dest='templates_glob', type=str, default=DEFAULT_TEMPLATE_GLOB,
        help=f'Templates glob pattern. Default: {DEFAULT_TEMPLATE_GLOB}'
    )
    parser.add_argument(
        '-trl', '--template-root-layout', dest='template_root_layout', type=str, default=DEFAULT_TEMPLATE_ROOT_LAYOUT,
        help=f'Template root layout file. Default: {DEFAULT_TEMPLATE_ROOT_LAYOUT}'
    )

    parser.add_argument(
        '-lrjs', '--live-reload-file', dest='live_reload_file', type=str, default=DEFAULT_LIVE_RELOAD_FILE,
        help=f'Live reload js file, relative to static folder. Default: {DEFAULT_LIVE_RELOAD_FILE}'
    )
    parser.add_argument(
        '-gcf', '--generated-css-file', dest='generated_css_file', type=str, default=DEFAULT_GENERATED_CSS_FILE,
        help=f'Generated css file, relative to static folder. Default: {DEFAULT_GENERATED_CSS_FILE}'
    )
    parser.add_argument(
        '-mcf', '--minified-css-file', dest='minified_css_file', type=str, default=DEFAULT_MINIFIED_CSS_FILE,
        help=f'Minified css file, relative to static folder. Default: {DEFAULT_MINIFIED_CSS_FILE}'
    )

    return parser


def generate_dev_script(static_folder: str, generated_css_file: str, minified_css_file: str):
    css_file_path = f'{static_folder}/{generated_css_file}'
    minified_css_file_path = f'{static_folder}/{minified_css_file}'
    return ("""
#!/usr/bin/env python

import websockets.server as ws_server
import websockets.legacy.protocol as ws_protocol
import asyncio
import datetime
import json
import subprocess
import os
import dotenv
import concurrent.futures
import platform
import argparse
import shlex


# docs:
# - https://websockets.readthedocs.io/en/stable/intro/tutorial2.html
# - https://websockets.readthedocs.io/en/stable/reference/asyncio/server.html

class _S:
    if platform.system() == 'Windows':
        os.system('color')

    BK = "\033[30m"
    R = "\033[31m"
    G = "\033[32m"
    BG = "\033[1;32m"
    Y = "\033[33m"
    B = "\033[34m"
    M = "\033[35m"
    C = "\033[36m"
    W = "\033[37m"
    ENDC = "\033[0;0m"
    NORMAL = "\033[1m"
    BOLD = "\033[1m"


def dev_print(*values: object):
    print(f'{_S.M}[dev]{_S.ENDC}', *values)


def int_or_default(value: 'str|None', default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


dotenv.load_dotenv()

LRWS_HOST = os.getenv('LIVE_RELOAD_WS_HOST', '127.0.0.1')
LRWS_PORT = int_or_default(os.getenv('LIVE_RELOAD_WS_PORT'), 5678)
TW_WATCH_PATH = os.getenv('TW_WATCH_PATH')
TW_INPUT_PATH_BUILD = os.getenv('TW_INPUT_PATH_BUILD')
TW_OUTPUT_PATH = os.getenv(
    'TW_OUTPUT_PATH', '""" + css_file_path + """'
)
TW_OUTPUT_PATH_BUILD = os.getenv(
    'TW_OUTPUT_PATH_BUILD', '""" + minified_css_file_path+"""'
)


LR_CONNECTIONS: 'set[ws_server.WebSocketServerProtocol]' = set()


async def handle_connection(websocket: ws_server.WebSocketServerProtocol):
    LR_CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        LR_CONNECTIONS.remove(websocket)


async def live_reload_server(host: str, port: int):
    async with ws_server.serve(handle_connection, host, port) as server:
        dev_print(
            f'Live reload {_S.G}ready{_S.ENDC} on {_S.C}ws://{host}:{_S.BOLD}{port}{_S.ENDC}')

        await server.wait_closed()

        dev_print(f'Live reload {_S.G}closed{_S.ENDC}')


def handle_tw_output(process: 'subprocess.Popen[bytes]'):
    if process.stdout is None:
        return

    for line in iter(process.stdout.readline, b''):
        if process.poll() is not None:
            break

        if (line.startswith(b'Done')):
            ws_protocol.broadcast(LR_CONNECTIONS, json.dumps({
                "type": "TRIGGER_FULL_RELOAD",
                "data": datetime.datetime.now().isoformat()
            }))

        print(f'{_S.C}[twcss]{_S.ENDC} {line.decode("utf-8")}', end='')


def handle_flask_output(process: 'subprocess.Popen[bytes]'):
    if process.stdout is None:
        return

    for line in iter(process.stdout.readline, b''):
        if process.poll() is not None:
            break

        print(f'{_S.G}[flask]{_S.ENDC} {line.decode("utf-8")}', end='')


async def dev_server(cli: argparse.Namespace):
    def live_reload_coroutine():
        if cli.no_live_reload or cli.no_tailwind:
            return None

        host = LRWS_HOST if cli.live_reload_host is None else cli.live_reload_host
        port = LRWS_PORT if cli.live_reload_port is None else cli.live_reload_port

        return live_reload_server(host, port)

    def tw_cli_executor(loop: asyncio.AbstractEventLoop, pool: concurrent.futures.ThreadPoolExecutor):
        if cli.no_tailwind:
            return None

        input_arg = f''
        if cli.tailwind_input is not None:
            input_arg = f'-i {cli.tailwind_input}'
        elif TW_WATCH_PATH is not None:
            input_arg = f'-i {TW_WATCH_PATH}'

        output_arg = f'-o {TW_OUTPUT_PATH}'
        if cli.tailwind_output is not None:
            output_arg = f'-o {cli.tailwind_output}'

        minify_arg = '--minify' if cli.tailwind_minify else ''

        cmd = f'tailwindcss --watch {input_arg} {output_arg} {minify_arg}'

        process = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        return loop.run_in_executor(pool, handle_tw_output, process)

    def flask_server_executor(loop: asyncio.AbstractEventLoop, pool: concurrent.futures.ThreadPoolExecutor):
        if cli.no_flask:
            return None

        host_arg = '--host' + cli.flask_host if cli.flask_host is not None else ''

        port_arg = '--port' + cli.flask_port if cli.flask_port is not None else ''

        debug_arg = '--debug' if cli.flask_mode == 'debug' else ''

        exclude_patterns = ['*/**/dev.py', '*/**/install_dev_mode.py']
        if cli.flask_exclude_patterns is not None:
            exclude_patterns.extend(cli.flask_exclude_patterns)
        exclude_patterns_arg = f'--exclude-patterns {";".join(exclude_patterns)}'

        cmd = f'flask run {host_arg} {port_arg} {debug_arg} {exclude_patterns_arg}'

        process = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        return loop.run_in_executor(pool, handle_flask_output, process)

    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        maybe_future_like = (
            live_reload_coroutine(),
            tw_cli_executor(loop, pool),
            flask_server_executor(loop, pool)
        )

        futures = (
            future
            for future in maybe_future_like
            if future is not None
        )

        _ = await asyncio.gather(*futures, return_exceptions=True)


def minify_tailwindcss(cli: argparse.Namespace):
    input_arg = f''
    if cli.input is not None:
        input_arg = f'-i {cli.input}'
    elif TW_INPUT_PATH_BUILD is not None:
        input_arg = f'-i {TW_INPUT_PATH_BUILD}'

    output_arg = f'-o {TW_OUTPUT_PATH_BUILD}'
    if cli.output is not None:
        output_arg = f'-o {cli.output}'

    minify_arg = ''
    if cli.minify is None or cli.minify is True:
        minify_arg = ' --minify'

    command = f'tailwindcss {input_arg} {output_arg} {minify_arg}'

    dev_print(f'Minifying tailwindcss for production...')

    build_result = subprocess.run(shlex.split(command))

    if build_result.returncode != 0:
        dev_print(f'Tailwind build for production {_S.R}fail{_S.ENDC}')
        return build_result.returncode

    dev_print(f'Tailwind build for production {_S.G}ready{_S.ENDC}')
    return build_result.returncode


def main():
    cli_args = cli().parse_args()

    if cli_args.command == 'build':
        exit(minify_tailwindcss(cli_args))

    asyncio.run(dev_server(cli_args))


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Enhanced dev environment for flask apps.',
        allow_abbrev=True
    )

    subparsers = parser.add_subparsers(
        title='commands', dest='command',
        help='availible commands',
        required=True
    )

    parser_build = subparsers.add_parser(
        name='build',
        description='Build the tailwindcss of the provided input as a single css file.',
        help='Build tailwindcss for production.',
        allow_abbrev=True
    )
    parser_build.add_argument(
        '-i', '--input', dest='input', type=str,
        help='Input path, accepts glob patterns.'
    )
    parser_build.add_argument(
        '-o', '--output', dest='output', type=str,
        help='Output path.'
    )
    build_minify_group = parser_build.add_mutually_exclusive_group()
    build_minify_group.add_argument(
        '--minify', dest='minify', action='store_true', default=None,
        help='Minify output.'
    )
    build_minify_group.add_argument(
        '--no-minify', dest='minify', action='store_false', default=None,
        help='Do not minify output.'
    )

    parser_dev = subparsers.add_parser(
        name='dev',
        description='''\
Extended dev mode for flask apps.
By default runs the flask app in debug mode,
tailwindcss in watch mode and live reload server.''',
        help='Run a development server.',
        allow_abbrev=True
    )
    parser_dev.add_argument(
        '--no-live-reload', dest='no_live_reload', action='store_true', default=False,
        help='Disable live reload server.'
    )
    parser_dev.add_argument(
        '-lrh', '--live-reload-host', dest='live_reload_host', type=str,
        help='Hostname for live reload server.'
    )
    parser_dev.add_argument(
        '-lrp', '--live-reload-port', dest='live_reload_port', type=int,
        help='Port for live reload server.'
    )

    parser_dev.add_argument(
        '--no-flask', dest='no_flask', action='store_true', default=False,
        help='Disable flask server.'
    )
    parser_dev.add_argument(
        '-fh', '--flask-host', dest='flask_host', type=str,
        help='Hostname for flask server.'
    )
    parser_dev.add_argument(
        '-fp', '--flask-port', dest='flask_port', type=int,
        help='Port for flask server.'
    )
    parser_dev.add_argument(
        '-fm', '--flask-mode',  dest='flask_mode', choices=('debug', 'no-debug'), default='debug',
        help='If debug mode is enabled, the flask server will be started with --debug flag. Default: debug.'
    )
    parser_dev.add_argument(
        '--flask-exclude-patterns', dest='flask_exclude_patterns', type=str, nargs='+',
        help='File exclude patterns for flask server. Base: */**/dev.py */**/install_dev_mode.py'
    )

    parser_dev.add_argument(
        '-nt', '--no-tailwind', dest='no_tailwind', action='store_true', default=False,
        help='Disable tailwindcss generation. If tailwindcss is disabled the live reload server will not be started.'
    )
    parser_dev.add_argument(
        '-ti', '--tailwind-input', dest='tailwind_input', type=str,
        help='Input path to watch for changes. Includes glob patterns.'
    )
    parser_dev.add_argument(
        '-to', '--tailwind-output', dest='tailwind_output', type=str,
        help='Output path for the generated css file.'
    )
    parser_dev.add_argument(
        '-tm', '--tailwind-minify', dest='tailwind_minify', action='store_true', default=False,
        help='Enables minification of the generated css file.'
    )

    return parser


if __name__ == "__main__":
    main()
""").lstrip()


JAVASCRIPT_LIVE_RELOAD_SCRIPT = '''
'use strict';


const VERBOSE = true;

/**
 * @param {'log'|'info'|'warn'|'error'} type
 * @param  {...any} args
 * @returns {void}
 */
function lrLog(type, ...args) {
  if (!VERBOSE) return;

  console[type](...args);
}

const WS_HOSTNAME = window.location.hostname;
const WS_PORT = 5678;
const WS_URL = `ws://${WS_HOSTNAME}:${WS_PORT}`;

/** @type {WebSocket|undefined} */
let lrWebSocket;

/** @type {ReturnType<setTimeout>|undefined} */
let lrwsCloseTimeout;

/**
 * @param {number=} code
 * @param {string=} reason
 * 
 * More: WebSocket error codes: https://www.rfc-editor.org/rfc/rfc6455.html#section-7.4
 */
function lrwsClose(code = 1000, reason = "Live reload") {
  lrWebSocket?.close(code, reason);
}


/** @type {ReturnType<setTimeout>|undefined} */
let lrwsReconnectTimeout;
let lrwsReconnectTimeoutCount = 0;

function lrwsAutoReconnect() {
  if (lrwsCloseTimeout) {
    clearTimeout(lrwsReconnectTimeout);
    return;
  }

  lrwsReconnectTimeoutCount++;
  lrLog("info", `Trying to reconnect to ${WS_URL}... (${lrwsReconnectTimeoutCount})`);
  lrwsInit();
}

function lrwsCancelAutoReconnect() {
  if (lrwsReconnectTimeout) {
    clearTimeout(lrwsReconnectTimeout);
    lrwsReconnectTimeout = undefined;
  }
}


function lrwsInit() {
  /** @type {WebSocket|undefined} */
  lrWebSocket = new WebSocket(WS_URL);

  lrWebSocket.addEventListener("open", () => {
    lrLog("info", `Connected to ${WS_URL}`);
  });

  lrWebSocket.addEventListener("message", (event) => {
    /** @type {unknown} */
    let msg;
    try {
      msg = JSON.parse(event.data);
      if (
        !msg || typeof msg !== 'object' ||
        !('type' in msg) ||
        typeof msg.type !== 'string'
      ) {
        lrLog("error", "Invalid message type", msg);
        return;
      }
    }
    catch (e) {
      lrLog("error", "Failed to parse message", e);
      return;
    }

    lrLog("log", "Received message", msg);

    if (msg.type === "TRIGGER_FULL_RELOAD") {
      if (lrwsCloseTimeout) {
        return;
      }

      lrwsCloseTimeout = setTimeout(() => {
        window.location.reload();
      }, 1000);

      return;
    }
  });

  lrWebSocket.addEventListener("close", (event) => {
    lrLog("info", `Disconnected from ${WS_URL}`);

    if (!lrwsCloseTimeout) {
      lrwsReconnectTimeout = setTimeout(
        lrwsAutoReconnect,
        (Math.floor(lrwsReconnectTimeoutCount / 10) + 1) * 5000
      );
    }
  });

  lrWebSocket.addEventListener("error", (event) => {
    if (event.currentTarget.readyState !== WebSocket.CLOSED) {
      lrLog("error", "WebSocket error", event);
    }
  });

  window.addEventListener('beforeunload', () => {
    lrwsClose()
  });
}

window.addEventListener("load", lrwsInit);
'''.lstrip()


if __name__ == "__main__":
    main()
