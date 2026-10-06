---
title: "OpenCode-boss"
---

### OpenCode-boss

[OpenCode](https://opencode.ai) is good at driving one machine. If you run `opencode serve` on more than one — a laptop, a workstation, a build box, three slices of the same project on three different hosts — you end up with several independent conversations and no way to see them at once from anywhere that isn't a desk.

opencode-boss is a coordinator for that. It lists the sessions across your fleet, sends a prompt to the host you name, and shows you the permission requests and diffs those sessions produce. There is a phone app for the parts you want away from the desk: the board, the inbox, and approving a permission.

It is MIT licensed, and the whole repository is public at [github.com/benthic-io/opencode-boss](https://github.com/benthic-io/opencode-boss). There is no closed server half.

### The coordinator runs no model

This is the part worth being precise about, because it is the part people get wrong.

The coordinator is a control plane. It writes down a dispatch, relays the prompt to the host you named, and relays back what came of it. It never calls a model, so it spends none of your tokens and there is no second bill anywhere.

The agent that does the actual thinking — the *boss* — is an ordinary OpenCode session running on your machine, on your account, with your settings. It reaches the coordinator through tools, exactly the way any other OpenCode session would.

### Your phone never holds a fleet password

A fleet password is the credential that lets opencode-boss reach one of your `opencode serve` instances. Those passwords live in the connector, on the machine that can already see the fleet. They are never sent to the coordinator, and they are never sent to your phone.

What the phone holds is one token for the coordinator. A worker on a fleet machine holds a different and much narrower credential, which can raise a signal and nothing else.

### What it does not do

- Not a mobile IDE. Reviewing a diff and approving a permission are in scope. Editing files and merging branches from a phone are not.
- Not a swarm. Sessions do not share context. The boss dispatches to them; it does not pretend they are talking to each other.
- Not a tunnel. Publishing a coordinator is the same ordinary problem as publishing any other service you run.

### Two ways to run it

One codebase and one feature set. The difference is configuration.

**Self-host.** The whole stack on a machine you control, nothing leaving your network. This is the default path in the documentation.

**Hosted, here.** A free coordinator at `https://benthic.io/boss`, which is the coordinator serving this page. You run a small outbound connector on a machine that can already reach your fleet; it dials out, so you never publish a port.

The connector reaches this coordinator over the public internet, so treat its token for what it is: a bearer credential for your fleet's board. One account, one password, no rate limiting on the login route.

### Status

Alpha. The repository is the product and the hosted coordinator is a deployment of it, not a separate build. The Android app is not on the Play Store yet; you build it from the repository.

### Why benthic.io is running it

We built opencode-boss to run our own OpenCode fleet, and it turned out to be generally useful rather than specifically ours, which is the same reason this site exists. So the coordinator is free and the software is MIT. If you would rather not depend on somebody else's machine, self-hosting is the better default anyway, and the documentation assumes you will.

Getting started, architecture, the API, the security model, and a troubleshooting page written from real failure modes are all in the repository.