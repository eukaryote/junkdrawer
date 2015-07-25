#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <hiredis/hiredis.h>

// gcc redis_queue_send_one.c -lhiredis


static const char * const KEYS[] = {
    "USER",
    "HOME"
};
static const int NUM_KEYS = 2;


/* Replace function of Albert Chan <albertmcchan@yahoo.com>,
 * from http://creativeandcritical.net/str-replace-c.
 */
char* replace_smart (const char *str, const char *sub, const char *rep)
{
    size_t slen = strlen(sub);
    size_t rlen = strlen(rep);
    size_t size = strlen(str) + 1;
    size_t diff = rlen - slen;
    size_t capacity = (diff>0 && slen) ? 2 * size : size;
    char *buf = malloc(capacity);
    char *find, *b = buf;

    if (b == NULL) return NULL;
    if (slen == 0) return memcpy(b, str, size);

    while((find = strstr(str, sub))) {
        if ((size += diff) > capacity) {
            char *ptr = realloc(buf, capacity = 2 * size);
            if (ptr == NULL) {free(buf); return NULL;}
            b = ptr + (b - buf);
            buf = ptr;
        }
        memcpy(b, str, find - str); /* copy up to occurrence */
        b += find - str;
        memcpy(b, rep, rlen);       /* add replacement */
        b += rlen;
        str = find + slen;
    }
    memcpy(b, str, size - (b - buf));
    b = realloc(buf, size);         /* trim to size */
    return b ? b : buf;
}


char * make_env_message(const int max_size)
{
    const int MAX_WRITE = max_size - 3;  // leaving room for {} and NULL

    char *buffer = malloc(max_size);
    char *envval, *escaped;
    int i, remaining, write_size, written = 1;

    buffer[0] = '{';
    for (i = 0; i < NUM_KEYS; i++) {
        envval = getenv(KEYS[i]);
        if (!envval)
            continue;

        remaining = MAX_WRITE - written;
        if (strstr(envval, "\"")) {
            escaped = replace_smart(envval, "\"", "\\\"");
        } else {
            escaped = 0;
        }
        write_size = snprintf(buffer + written, remaining, "%s\"%s\":\"%s\"",
                              written > 1 ? "," : "", KEYS[i],
                              escaped ? escaped: envval);
        if (escaped)
            free(escaped);

        if (write_size >= remaining)
        {
            printf("max size (%d bytes) exceeded\n", max_size);
            free(buffer);
            return 0;
        }
        written += write_size;
    }
    buffer[written] = '}';
    buffer[written + 1] = 0;
    buffer = realloc(buffer, written + 1);
    return buffer;
}


redisContext * redis_connect(const char *hostname, const int port)
{
    redisContext *c;
    c = redisConnect(hostname, port);
    if (c == NULL || c->err)
    {
        if (c)
        {
            printf("Connection error: %s\n", c->errstr);
            redisFree(c);
        } else {
            printf("Connection error: can't allocate redis context\n");
        }
        exit(1);
    }
    return c;
}


int main(int argc, char **argv)
{
    const char *hostname = "127.0.0.1";
    const int port = 6379;
    const char *db = "2";

    redisReply *reply;
    redisContext *c = redis_connect(hostname, port);

    // choose database
    reply = redisCommand(c, "SELECT %s", db);
    if (!reply || reply->type == REDIS_REPLY_ERROR) {
        if (reply) {
            printf("redis error: %s\n", reply->str);
        }
        return 1;
    }

    // generate JSON message
    char *message = make_env_message(607);
    if (!message) {
        redisFree(c);
        return 1;
    }

    // send and print response, which is number of items in list
    reply = redisCommand(c, "LPUSH %s %s", "cevents", message);
    printf("%lld\n", reply->integer);

    free(message);
    freeReplyObject(reply);
    redisFree(c);

    return 0;
}
