FROM node:22-alpine
LABEL authors="ndy40"

WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

RUN apk update  && npm i -g npm@latest \
    && addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --chown=nextjs:nodejs package.json  /app/
RUN npm install

COPY --chown=nextjs:nodejs . /app

USER nextjs

EXPOSE 3000

CMD ["npm", "run", "dev"]