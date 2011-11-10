import mucam_api as api
import mucam_ui as ui

if __name__ == '__main__':
  c = api.Controller(echo=False)
  ui.addUser(c)

