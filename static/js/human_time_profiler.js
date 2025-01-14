// askNotificationPermission copied on 2025-01-11 from https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications_API
function askNotificationPermission() {
  // Check if the browser supports notifications
  if (!("Notification" in window)) {
    console.log("This browser does not support notifications.");
    return;
  }
  const notificationBtn = document.getElementById("notificationBtn");
  Notification.requestPermission().then((permission) => {
    // set the button to shown or hidden, depending on what the user answers
    notificationBtn.style.display = permission === "granted" ? "none" : "block";
  });
}

function sendNotificationsAtRandom(minTimeToNextNotifMS, maxTimeToNextNotifMS) {
  const curTime = new Date();
  const curTimeString = curTime.toString();
  const text = 'What were you doing at ' + curTimeString + '?';
  const notification = new Notification("Human Time Profiler", { body: text });
  notification.onclick = notificationClickHandler;

  const entry = document.createElement('li');
  entry.appendChild(document.createTextNode(curTimeString));
  document.getElementById("timeList").prepend(entry);

  const randomMillis = Math.random() * (maxTimeToNextNotifMS - minTimeToNextNotifMS) + minTimeToNextNotifMS;
  setTimeout(sendNotificationsAtRandom, randomMillis, minTimeToNextNotifMS, maxTimeToNextNotifMS)
}

function notificationClickHandler(event) {
  console.log(event);

  window.open(document.getElementById("linkToOpen").value);
}

const MILLIS_PER_SECOND = 1000;
const MILLIS_PER_DAY = 24 * 60 * 60 * 1000;
sendNotificationsAtRandom(MILLIS_PER_SECOND, MILLIS_PER_DAY)
