package gov.nasa.jpf.jvm;

import java.util.Random;


public class Verify
{
  private static Random random;
  /**
   * Returns a random number between 0 and max inclusive.
   */
  public static int random (int max) {
    // this is only executed when not running JPF
    if (random == null) {
      random = new Random();
    }
    return random.nextInt(max + 1);
  }

  public static void beginAtomic()
  {
  }

  public static void endAtomic()
  {
  }
}