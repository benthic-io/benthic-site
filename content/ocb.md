---
title: "ocb"
---

### ocb

[OpenCode](https://opencode.ai) is good at driving one machine. Run `opencode serve` on more than one — a laptop, a workstation, a build box, three slices of the same project on three hosts — and you get several independent conversations and no way to see them together from anywhere but a desk.

ocb is the coordinator for that fleet. It lists every session across every host, sends a prompt to the host you name, and shows the permission requests, questions, and changes those sessions produce. The phone app carries the parts you want away from the desk: the board, the inbox, and the answer to a waiting session.

It is MIT licensed and the whole repository is public at
[github.com/benthic-io/opencode-boss](https://github.com/benthic-io/opencode-boss). There is no closed server half.

### Built for a team, not a queue

A fleet is not one conversation running in parallel with itself. It is a team: a session that owns the app, one that owns the daemons, one that owns deployment, one that owns the docs, and a boss that coordinates them. Each has a scope and a set of files it may change.

The board, the inbox, and the signal queue are how that team reaches a human. They are also the layer the next step builds on.

**Swarm capability is in development.** The direction is session-to-session coordination: every member sees the roster — who else is on the team, what each owns, and what each can be asked to do — and a change that crosses a boundary is announced to the member who now has work, with the contract and the files, instead of being discovered at merge time. A UI change that alters an API call tells the backend session; a backend change that moves a route tells the app and the docs. The coordinator stays a control plane: it carries the message, it does not call a model.

### The coordinator runs no model

The coordinator writes down a dispatch, relays the prompt to the host you named, and relays back what came of it. It never calls a model, so it spends none of your tokens and there is no second bill.

The agent doing the thinking is an ordinary OpenCode session on your machine, on your account, with your settings. It reaches the coordinator through tools, exactly the way any other session would.

### Your phone never holds a fleet password

Fleet credentials live in the connector, on the machine that can already see the fleet. They are never sent to the coordinator and never sent to your phone. What the phone holds is one token for the coordinator; a worker on a fleet machine holds a narrower credential that can raise a signal and nothing else.

### What it does not do

- Not a mobile IDE. Reviewing changes and answering a permission are in scope. Editing files and merging branches from a phone are not.
- Not a tunnel. Publishing a coordinator is the ordinary problem of publishing any service you run.

### Two ways to run it

One codebase and one feature set; the difference is configuration.

**Self-host.** The whole stack on a machine you control, nothing leaving your network. This is the default path in the documentation.

**Hosted, here.** A free coordinator at `https://benthic.io/boss` — note that `/boss` is the coordinator's path, separate from this page. You run a small outbound connector on a machine that can already reach your fleet; it dials out, so you never publish a port.

### Status

Alpha. The repository is the product and the hosted coordinator is a deployment of it, not a separate build. The Android app is not on the Play Store yet; you build it from the repository.

### Why benthic.io runs it

We built ocb to run our own OpenCode fleet, and it turned out to be generally useful rather than specifically ours — the same reason this site exists. The software is MIT and the hosted coordinator is free. If you would rather not depend on somebody else's machine, self-hosting is the better default, and the documentation assumes you will.

Getting started, architecture, the API, the security model, and a troubleshooting page written from real failure modes are in the repository.
