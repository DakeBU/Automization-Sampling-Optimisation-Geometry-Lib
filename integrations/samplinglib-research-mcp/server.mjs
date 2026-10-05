import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const dataPath = resolve(
  process.env.ASTIS_WORKSPACE_DATA ?? "data/research-workspaces.json",
);
const widgetHtml = readFileSync(
  new URL("./public/workspace-widget.html", import.meta.url),
  "utf8",
);
const payload = JSON.parse(readFileSync(dataPath, "utf8"));
const workspaces = payload.workspaces ?? [];

const findWorkspace = (id) => workspaces.find((row) => row.id === id);
const findTheorem = (workspace, id) =>
  workspace?.theorems?.find((row) => row.id === id);
const findStep = (theorem, id) => theorem?.steps?.find((row) => row.id === id);

const outputSchema = {
  view: z.string(),
  workspaces: z.array(z.any()).optional(),
  workspace: z.any().optional(),
  theorem: z.any().optional(),
  step: z.any().optional(),
  packet: z.any().optional(),
};

const reply = (view, values, message) => ({
  content: [{ type: "text", text: message }],
  structuredContent: { view, ...values },
});

function createResearchServer() {
  const server = new McpServer({
    name: "samplinglib-research-workspace",
    version: "0.1.0",
  });

  registerAppResource(
    server,
    "samplinglib-research-widget",
    "ui://samplinglib/research-workspace.html",
    {},
    async () => ({
      contents: [
        {
          uri: "ui://samplinglib/research-workspace.html",
          mimeType: RESOURCE_MIME_TYPE,
          text: widgetHtml,
        },
      ],
    }),
  );

  const meta = { ui: { resourceUri: "ui://samplinglib/research-workspace.html" } };

  registerAppTool(
    server,
    "list_research_workspaces",
    {
      title: "List Samplinglib research workspaces",
      description:
        "Lists source-pinned Samplinglib proof workspaces without claiming that open paper theorems are formalized.",
      inputSchema: {},
      outputSchema,
      _meta: meta,
    },
    async () =>
      reply(
        "workspace-list",
        {
          workspaces: workspaces.map(({ id, title, role, status, source_records }) => ({
            id,
            title,
            role,
            status,
            source_records,
          })),
        },
        `Found ${workspaces.length} source-pinned Samplinglib research workspaces.`,
      ),
  );

  registerAppTool(
    server,
    "open_research_workspace",
    {
      title: "Open a Samplinglib research workspace",
      description:
        "Returns the readable theorem route, assumptions, proof steps and bookkeeping ledger for one exact source case.",
      inputSchema: {
        workspace_id: z.string().min(1),
        theorem_id: z.string().optional(),
      },
      outputSchema,
      _meta: meta,
    },
    async ({ workspace_id, theorem_id }) => {
      const workspace = findWorkspace(workspace_id);
      if (!workspace) return reply("error", {}, `Unknown workspace: ${workspace_id}`);
      const theorem = theorem_id ? findTheorem(workspace, theorem_id) : undefined;
      if (theorem_id && !theorem) {
        return reply("error", {}, `Unknown theorem ${theorem_id} in ${workspace_id}.`);
      }
      return reply(
        "workspace",
        { workspace, theorem },
        `Opened ${workspace.title}. AI output remains unverified; inspect each explicit truth boundary.`,
      );
    },
  );

  registerAppTool(
    server,
    "get_proof_step",
    {
      title: "Inspect one Samplinglib proof step",
      description:
        "Returns one exact mathematical proof step with its source anchor, assumptions, open boundary and compiled reusable support.",
      inputSchema: {
        workspace_id: z.string().min(1),
        theorem_id: z.string().min(1),
        step_id: z.string().min(1),
      },
      outputSchema,
      _meta: meta,
    },
    async ({ workspace_id, theorem_id, step_id }) => {
      const workspace = findWorkspace(workspace_id);
      const theorem = findTheorem(workspace, theorem_id);
      const step = findStep(theorem, step_id);
      if (!workspace || !theorem || !step) {
        return reply("error", {}, "The requested workspace, theorem, or step was not found.");
      }
      return reply(
        "proof-step",
        { workspace, theorem, step },
        `${step.title}: ${step.explanation}\n\nLean status: ${step.status}.`,
      );
    },
  );

  registerAppTool(
    server,
    "export_verification_packet",
    {
      title: "Export a bounded verification packet",
      description:
        "Packages one proof step for a Codex/Lean session while preserving source, assumptions, evidence status and residual boundary.",
      inputSchema: {
        workspace_id: z.string().min(1),
        theorem_id: z.string().min(1),
        step_id: z.string().min(1),
        proposed_claim: z.string().optional(),
      },
      outputSchema,
      _meta: meta,
    },
    async ({ workspace_id, theorem_id, step_id, proposed_claim }) => {
      const workspace = findWorkspace(workspace_id);
      const theorem = findTheorem(workspace, theorem_id);
      const step = findStep(theorem, step_id);
      if (!workspace || !theorem || !step) {
        return reply("error", {}, "The requested workspace, theorem, or step was not found.");
      }
      const packet = {
        schema_version: "1.0",
        project: payload.project,
        workspace_id,
        theorem: {
          id: theorem.id,
          title: theorem.title,
          statement: theorem.statement,
          formula: theorem.formula,
          assumptions: theorem.assumptions,
          boundary: theorem.boundary,
        },
        proof_step: step,
        proposed_claim: proposed_claim ?? "",
        evidence: workspace.evidence_contract,
        required_next_gates: [
          "exact Lean elaboration or compilation",
          "focused tests",
          "independent source-fidelity review",
          "ASTIS admission before blue status",
        ],
      };
      return reply(
        "verification-packet",
        { workspace, theorem, step, packet },
        "Exported a bounded candidate packet. It is not a proof certificate.",
      );
    },
  );

  return server;
}

const port = Number(process.env.PORT ?? 8787);
const host = process.env.HOST ?? "127.0.0.1";
const MCP_PATH = "/mcp";

const httpServer = createServer(async (req, res) => {
  if (!req.url) return res.writeHead(400).end("Missing URL");
  const url = new URL(req.url, `http://${req.headers.host ?? "localhost"}`);
  if (req.method === "OPTIONS" && url.pathname === MCP_PATH) {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id",
      "Access-Control-Expose-Headers": "Mcp-Session-Id",
    });
    return res.end();
  }
  if (req.method === "GET" && url.pathname === "/") {
    return res
      .writeHead(200, { "content-type": "text/plain; charset=utf-8" })
      .end("Samplinglib read-only research workspace MCP App");
  }
  if (
    url.pathname === MCP_PATH &&
    req.method &&
    new Set(["POST", "GET", "DELETE"]).has(req.method)
  ) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");
    const server = createResearchServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });
    res.on("close", () => {
      transport.close();
      server.close();
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch (error) {
      console.error("Samplinglib MCP request failed:", error);
      if (!res.headersSent) res.writeHead(500).end("Internal server error");
    }
    return;
  }
  res.writeHead(404).end("Not Found");
});

httpServer.listen(port, host, () => {
  console.log(`Samplinglib research MCP App: http://${host}:${port}${MCP_PATH}`);
  console.log("Read-only: no Lean execution, repository writes, or proof admission.");
});
