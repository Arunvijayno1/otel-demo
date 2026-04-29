'use strict';

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { PrometheusExporter } = require('@opentelemetry/exporter-prometheus');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { resourceFromAttributes } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

// Trace exporter
const traceExporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});

// Metrics exporter
const prometheusExporter = new PrometheusExporter({
  port: 9464,
});

// SDK setup
const sdk = new NodeSDK({
  traceExporter: traceExporter,

  // ✅ FIX: use metricReaders (not metricReader)
  metricReaders: [prometheusExporter],

  // ✅ FIX: restore full auto instrumentation
  instrumentations: [getNodeAutoInstrumentations()],

  resource: resourceFromAttributes({
    [SemanticResourceAttributes.SERVICE_NAME]: 'order-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'dev',
  }),
});

sdk.start();

console.log("OpenTelemetry fully configured (Tracing + Metrics)");