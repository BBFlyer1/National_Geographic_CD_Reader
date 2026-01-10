# -*- coding: utf-8 -*-
"""
Drive listener class for NGS CD Reader.

Source: https://abdus.dev/posts/python-monitor-usb/
Created on Wed Dec 29 13:55:07 2024.

@author: Bob
"""
#
# Create a class that interacts with Tkinter and monitors itself.
from threading import Thread

import os
import queue
import time


class MonitoredWorker:
    """
    Monitor a threaded worker with a queue listener.

    A class that does work and causes a (tkinter) App to schedule monitoring
    of the results queue.

    Internally, this class creates a worker and passes it to a thread for
    execution. At the same time, this class schedules the App to
    monitor the queue.
    """

    def __init__(self, app):
        self.app = app
        self.queue = queue.Queue()  # The queue is internal to this class.

    def start(self):
        """Start the worker thread."""
        self.thread = Thread(target=self.worker_thread)
        # Daemonize thread insures cleanup when the main program exits.
        self.thread.daemon = True
        self.thread.start()
        # Start the monitor for the queue.
        # when I used this, it caused a recursion depth error.
        # self.app.after(100, self.monitor_queue)

    def worker_thread(self):
        """
        Worker place holder for a thread which generates events.

        The Application needs to extend the Monitored Worker class
        to implement a worker thread that will monitor whatever event
        the Application needs monitored.  When the worker detects
        the event, it is put onto a queue to be transferred back to
        the calling application.  The thread is started when the object
        is created.

        Here is an example of a worker code:
        while True:
            if os.path.exists(self.path):
                status = 'closed'
            else:
                status = 'open'
            if self.cdrom_drive_status != status:
                self.cdrom_drive_status = status
                s_event = f"CDROM drawer {self.cdrom_drive_status}"
                self.queue.put(s_event)
            time.sleep(1)  # Simulate some work being done
        The critical piece of the above code is the line
        "self.queue.put(s_event)" which puts the appropriate value
        of whatever happens that we are monitoring into a queue that
        the app monitors in the main queue.

        Returns
        -------
        queue event
            When the worker thread detects an event, notification is
            put on a queue that was passed to the MonitoredWorker class
            from the calling Application on its initialization.

        """
        pass

    def monitor_queue(self):
        """
        Process events from the queue.

        Process events and pass them to the application app to
        do something with.

        Returns
        -------
        None.

        """
        while not self.queue.empty():
            results = self.queue.get()
            self.app.process_results(results)
        # Check the queue again after 100ms
        self.app.after(100, self.monitor_queue)

# %% CDROM drawer monitor class implements monitored worker.


class cdrom_drawer_monitor(MonitoredWorker):
    """
    Implement a CDROM Drawer Monitor for the NGS App.

    Extends the MonitoredWorker class to implement a CDROM drawer open
    or closed monitor.  Closed includes a test of whether a National
    Geographic Society CD in the drive.

    """

    def __init__(self, app):
        super().__init__(app)
        # not to be confused with app.CD we use a different variable
        # here to keep app thread and monitor thread separate.
        self._drive_has_ngs_cd = False

        self.path = "D:/IMAGES"

        self._cd_state()
        app.process_results(self._drive_has_ngs_cd)
        try:
            self.path = app.ng_base_path
        except:
            pass

    def worker_thread(self):
        """
        Worker thread generates CDROM drawer open and close events.

        It operates in an endless loop as long as the application is
        running.

        Returns
        -------
        s_event: bool
            Put results on internal queue which is monitored by
            calling app.  True is when the CDROM drive drawer is
            closed and a National Geographic Society CD is loaded.
            False indicates the drawer is open or the loaded CD
            is not one of the National Geographic Society CDs.
        """
        while True:
            self._cd_state()
            """
            if os.path.exists(self.path):
                status = True
            else:
                status = False
            if self._drive_has_ngs_cd != status:
                self._drive_has_ngs_cd = status
                s_event = self._drive_has_ngs_cd
                self.queue.put(s_event)"""
            time.sleep(1)  # wait one second before testing again.

    def _cd_state(self):
        if os.path.exists(self.path):
            status = True
        else:
            status = False
        if self._drive_has_ngs_cd != status:
            self._drive_has_ngs_cd = status
            s_event = self._drive_has_ngs_cd
            self.queue.put(s_event)

    def get(self):
        """
        Return the current cdrom drive status.

        Return the current CDROM Drive status.

        False, means the cdrom drive door is open or a non NGS CD is in
        the drive.

        True, means the cdrom drive door is shut and the drive contains a
        NGS Society CD.

        Returns
        -------
        bool
            Returns True or False status of NGC CD in CDROM drawer.

        """
        return self.app.CD
