// Required includes
#include "pico/stdlib.h"
#include <stdio.h>

// getchar_timeout_us returns a int32 -1 if nothing is read
// since we are using a char this is 255
#define ENDSTDIN 255

/**
 * @brief Read stdin until CR or LF is received or the buffer length is meet.
 * This function is non blocking and utilizes the string buffer provided to
 * store input between calls. Returns length of line read (not including the
 * line terminator) or -1 if no line end is available.
 *
 * @param str char buffer to store read characters in
 * @param len length of buffer pointed to by str
 * @param timeout_ms how long to wait for input
 * @return Number or characters in line or -1 if no newline
 */
int getline_timeout_ms(char *str, uint32_t len, uint32_t timeout_ms);

int getline_timeout_ms(char *str, uint32_t len, uint32_t timeout_ms) {
  // static char str[50];
  char chr = getchar_timeout_us(0);
  static int lp = 0;

  absolute_time_t timeout = make_timeout_time_ms(timeout_ms);

  while (!(chr == ENDSTDIN && time_reached(timeout))) {
    if (chr != ENDSTDIN) {
      str[lp++] = chr;
      // printf("%c", chr);
      if (chr == '\r' || chr == '\n' || lp == len) {
        str[lp] = 0; // terminate string
        // printf("You wrote - %s\n", str);
        // memset(strg, 0, sizeof(strg));
        int length = lp - 1;
        lp = 0; // reset string buffer pointer
        return length;
      }
    }

    chr = getchar_timeout_us(0);
  }
  return -1;
}