require('./tracing'); // MUST be first

const express = require('express');
const { context, trace } = require('@opentelemetry/api');
const pino = require('pino');

const app = express();

/* =========================
   Logger (writes to file)
========================= */
const logger = pino(
  pino.destination({
    dest: './app.log',
    sync: false
  })
);

/* =========================
   Helper: Extract trace info
========================= */
function getTraceInfo() {
  const span = trace.getSpan(context.active());

  if (!span) return {};

  const spanContext = span.spanContext();

  return {
    trace_id: spanContext.traceId,
    span_id: spanContext.spanId
  };
}



app.get('/test-trace', (req, res) => {
  const tracer = trace.getTracer('manual-test');

  const span = tracer.startSpan('manual-span');
  span.end();

  res.send("manual trace created");
});
/* =========================
   Routes
========================= */

// Health check
app.get('/health', (req, res) => {
  logger.info({
    ...getTraceInfo(),
    msg: "Health check"
  });

  res.json({ status: "ok" });
});


// Orders API
app.get('/orders', (req, res) => {
  const traceInfo = getTraceInfo();

  // Simulate failure
  if (req.query.fail === 'true') {
    logger.error({
      ...traceInfo,
      msg: "Simulated failure"
    });

    return res.status(500).json({
      error: "Simulated failure"
    });
  }

  // Normal flow
  logger.info({
    ...traceInfo,
    msg: "Fetching orders"
  });

  res.json([
    { id: 1, item: "Laptop" },
    { id: 2, item: "Phone" }
  ]);
});


/* =========================
   Global Error Handler (important)
========================= */
app.use((err, req, res, next) => {
  logger.error({
    ...getTraceInfo(),
    msg: err.message
  });

  res.status(500).json({
    error: "Internal Server Error"
  });
});


/* =========================
   Start Server
========================= */
app.listen(3000, () => {
  console.log("Server running on port 3000");
});