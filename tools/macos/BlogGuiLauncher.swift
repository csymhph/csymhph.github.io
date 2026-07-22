import AppKit

final class BlogGuiLauncherDelegate: NSObject, NSApplicationDelegate {
    private var receivedURL = false
    private var launched = false

    func applicationWillFinishLaunching(_ notification: Notification) {
        NSAppleEventManager.shared().setEventHandler(
            self,
            andSelector: #selector(handleGetURLEvent(_:withReplyEvent:)),
            forEventClass: AEEventClass(kInternetEventClass),
            andEventID: AEEventID(kAEGetURL)
        )
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        // Double-clicking the launcher app remains a supported local entrypoint.
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.35) { [weak self] in
            guard let self, !self.receivedURL else { return }
            self.launchWritingStudio()
        }
    }

    @objc private func handleGetURLEvent(
        _ event: NSAppleEventDescriptor,
        withReplyEvent replyEvent: NSAppleEventDescriptor
    ) {
        receivedURL = true
        guard
            let rawURL = event.paramDescriptor(forKeyword: keyDirectObject)?.stringValue,
            let url = URL(string: rawURL),
            url.scheme == "csymhph-blog",
            url.host == "open",
            url.path.isEmpty || url.path == "/"
        else {
            NSApplication.shared.terminate(nil)
            return
        }
        launchWritingStudio()
    }

    private func launchWritingStudio() {
        guard !launched else { return }
        launched = true

        let logPath = "/private/tmp/csymhph-blog-gui-launcher.log"
        FileManager.default.createFile(atPath: logPath, contents: nil)
        let logHandle = FileHandle(forWritingAtPath: logPath) ?? FileHandle.nullDevice
        let executableURL = URL(fileURLWithPath: CommandLine.arguments[0]).standardizedFileURL
        let contentsURL = executableURL.deletingLastPathComponent().deletingLastPathComponent()
        let infoURL = contentsURL.appendingPathComponent("Info.plist")
        guard
            let info = NSDictionary(contentsOf: infoURL),
            let launcherPath = info["BlogGuiLauncherPath"] as? String
        else {
            logHandle.write(Data("Missing BlogGuiLauncherPath in \(infoURL.path)\n".utf8))
            NSApplication.shared.terminate(nil)
            return
        }

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/nohup")
        process.arguments = ["/bin/bash", launcherPath]
        process.standardOutput = logHandle
        process.standardError = logHandle

        do {
            try process.run()
        } catch {
            NSSound.beep()
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            NSApplication.shared.terminate(nil)
        }
    }
}

let application = NSApplication.shared
let delegate = BlogGuiLauncherDelegate()
application.delegate = delegate
application.setActivationPolicy(.accessory)
application.run()
