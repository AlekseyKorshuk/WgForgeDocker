from modules.core.source import attach_core_module

attach_core_module()

from modules.core.source import server, app

if __name__ == '__main__':
    app.run_server(debug=True)
