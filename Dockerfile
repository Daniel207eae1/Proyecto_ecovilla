# Create app
FROM grafana/grafana:latest

# Maintainer
LABEL maintainer="Julian Colorado <julian.coloradoa@upb.edu.co>"

# Copy plugins and rewrite defaults.ini file to allow loading unsigned plugins
USER root

COPY ./customplugins /var/lib/customplugins

RUN sed -i "s|;allow_loading_unsigned_plugins =|allow_loading_unsigned_plugins = e-2030-smart-grid-unifilar-plugin |g" /etc/grafana/grafana.ini
RUN sed -i "s|;plugins = /var/lib/grafana/plugins|plugins = /var/lib/customplugins/|g" /etc/grafana/grafana.ini

# Expose port
EXPOSE 3000
