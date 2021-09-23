if __name__ == '__main__':
  parser = argparse.ArgumentParser("LED Matrix clear program")
  parser.add_argument("-d", "--debug", action='store_true', help="Enable debug output")
  args = parser.parse_args()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  m = LEDMatrix()
  s = Screen(8,32,m)
  s.clear()
  s.update()
