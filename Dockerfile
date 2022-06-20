FROM node:16-alpine AS runner

RUN apk add --no-cache libc6-compat
RUN apk add --no-cache git
RUN apk add bash

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
RUN npm install typescript @types/node eslint eslint-config-next 

COPY run.sh ./
COPY update.py ./

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

EXPOSE 57896

ENV PORT 57896

ENV DATABASE_URL "postgresql://expenses:stsRover44@192.168.0.50:5432/expensesprod?schema=public"

CMD ["/bin/sh", "run.sh"]