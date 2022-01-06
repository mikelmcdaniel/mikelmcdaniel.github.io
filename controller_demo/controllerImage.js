class ControllerImage {
  // slotNames and slotValues are used to map to files.
  // slotValues specifies which types of things can go in that slot.
  slotNames = ["Base", "1", "2", "3", "4"];
  slotValues = [
    ["Controller", "ControllerUglyOrange"],
    ["DP", "FB", "JS"],
    ["DP", "FB", "JS"],
    ["DP", "FB", "JS"],
    ["DP", "FB", "JS"]];
  // TODO: It would be nice if these didn't need to be hard-coded...
  // slotCoords and maxSlotRadius are used for mapping a 2d point to
  // the nearest slot (for UI purposes).
  slotCoords = [
    { x: null, y: null },
    { x: 336, y: 154 },
    { x: 336, y: 334 },
    { x: 520, y: 456 },
    { x: 766, y: 372 }];
  maxSlotRadius = 150;

  // Stateful UI
  // selectedSlot is null when no slot is selected.
  // Any functions using selectedSlot should handle null!
  selectedSlot = null;
  mode = null;
  demoTimer = null;

  div = null;
  baseImg = null;
  slotImgs = null;
  slotIndices = null;

  constructor(divID, imgRootURL="") {
    this.imgRootURL = imgRootURL;
    this.div = document.getElementById(divID);

    // Initialize slot info from HTML.
    this.slotImgs = [];
    this.slotIndices = [];
    for (let sni = 0; sni < this.slotNames.length; ++sni) {
      let img = document.getElementById(this.div.id + ".img" + sni);
      this.slotImgs.push(img);
      let indices = this.indicesFromImgSrc(img.src);
      console.assert(indices.slotNameIndex == sni);
      this.slotIndices.push(indices.slotValueIndex);
      // Ensure HTML is using the same exact imgSrc, that will be used when the slots are changed!
      // This isn't necessary but helps catch bugs sooner.
      console.assert(this.slotImgs[sni].src == this.imgSrc(sni, this.slotIndices[sni]));
    }
    this.baseImg = this.slotImgs[0];
    ControllerImage.setMode(this, 'interactive');
  }

  imgSrcBaseName(slotNameIndex, slotValueIndex) {
    return this.slotValues[slotNameIndex][slotValueIndex] + this.slotNames[slotNameIndex] + ".png";
  }

  imgSrc(slotNameIndex, slotValueIndex) {
    return this.imgRootURL + this.imgSrcBaseName(slotNameIndex, slotValueIndex);
  }

  static baseName(urlStr) {
    const url = new URL(urlStr);
    const urlParts = url.pathname.split("/");
    return urlParts[urlParts.length - 1];
  }

  indicesFromImgSrc(imgSrc) {
    const imgSrcBaseName = ControllerImage.baseName(imgSrc)
    // TODO: This could be more efficient!
    for (let sni = 0; sni < this.slotValues.length; ++sni) {
      for (let svi = 0; svi < this.slotValues[sni].length; ++svi) {
        if (this.imgSrcBaseName(sni, svi) == imgSrcBaseName) {
          return { slotNameIndex: sni, slotValueIndex: svi };
        }
      }
    }
    throw new RangeError("Could not determine slots for " + imgSrc);
  }

  closestSlot(pixelX, pixelY) {
    let slotIndex = 0;
    let closestDistance = Infinity;
    for (let sni = 0; sni < this.slotCoords.length; ++sni) {
      const cx = this.slotCoords[sni].x;
      const cy = this.slotCoords[sni].y;
      const d = Math.sqrt(Math.pow(pixelX - cx, 2) + Math.pow(pixelY - cy, 2));
      if (d < closestDistance) {
        slotIndex = sni;
        closestDistance = d;
      }
    }
    return closestDistance <= this.maxSlotRadius ? slotIndex : 0;
  }

  // Change what's in a given slot.
  // e.g. incrementSlotValue(0) might change slot 0 from a D-Pad to a Joy Stick.
  setSlot(slotNameIndex, slotValueIndex) {
    if (slotNameIndex === null) {
      return;
    }
    this.slotIndices[slotNameIndex] = slotValueIndex;
    this.slotImgs[slotNameIndex].src = this.imgSrc(slotNameIndex, slotValueIndex);
  }

  incrementSlotValue(slotNameIndex) {
    if (slotNameIndex === null) {
      return;
    }
    const newSlotValueIndex = (this.slotIndices[slotNameIndex] + 1) % this.slotValues[slotNameIndex].length;
    this.setSlot(slotNameIndex, newSlotValueIndex);
  }

  decrementSlotValue(slotNameIndex) {
    if (slotNameIndex === null) {
      return;
    }
    const newSlotValueIndex = (this.slotIndices[slotNameIndex] + this.slotValues[slotNameIndex].length - 1) % this.slotValues[slotNameIndex].length;
    this.setSlot(slotNameIndex, newSlotValueIndex);
  }

  pixelCoordsFromMouseEvent(event) {
    // Modified from https://stackoverflow.com/a/58568016/5673832
    let bounds = this.baseImg.getBoundingClientRect();
    let x = event.clientX - bounds.left;
    let y = event.clientY - bounds.top;
    let scaleFactor = getComputedStyle(this.div).getPropertyValue('--scaleFactor');
    let cw = this.baseImg.clientWidth * scaleFactor;
    let ch = this.baseImg.clientHeight * scaleFactor;
    let iw = this.baseImg.naturalWidth;
    let ih = this.baseImg.naturalHeight;
    let px = Math.round(x / cw * iw);
    let py = Math.round(y / ch * ih);
    return { x: px, y: py };
  }

  //
  // Stateful UI
  //

  highlightSelectedSlot() {
    if (this.selectedSlot === null) {
      for (let sni = 0; sni < this.slotImgs.length; ++sni) {
        this.slotImgs[sni].style.opacity = 1.0;
      }
    } else {
      for (let sni = 0; sni < this.slotImgs.length; ++sni) {
        this.slotImgs[sni].style.opacity = 0.5;
      }
      this.slotImgs[this.selectedSlot].style.opacity = 1.0;
    }
  }

  setSelectedSlot(selectedSlotIndex) {
    this.selectedSlot = selectedSlotIndex;
    this.highlightSelectedSlot();
  }

  incrementSelectedSlotValue() {
    this.incrementSlotValue(this.selectedSlot);
  }

  decrementSelectedSlotValue() {
    this.decrementSlotValue(this.selectedSlot);
  }

  incrementSelectedSlot() {
    this.setSelectedSlot((this.selectedSlot + 1) % this.slotNames.length)
  }

  decrementSelectedSlot() {
    this.setSelectedSlot((this.selectedSlot + numSlots - 1) % numSlots)
  }

  randomlyChangeARandomSlot() {
    const numSlots = this.slotNames.length
    const randomSlot = Math.floor(Math.random() * numSlots);
    const numSlotValues = this.slotValues[randomSlot].length;
    const randomSlotValue = (this.slotIndices[randomSlot] + Math.floor(Math.random() * (numSlotValues - 1)) + 1) % numSlotValues;
    this.setSlot(randomSlot, randomSlotValue);
  }

  //
  // Event Handlers
  //

  static setMode(self, mode, modeOptions) {
    // Disable old mode (if applicable)
    if (self.mode == 'demo') {
      clearInterval(self.demoTimer);
    }
    // Enable new mode
    if (mode == 'interactive') {
      self.div.onmousedown = function (event) { ControllerImage.onClick(controllerImage, event); }
      self.div.onwheel = function (event) { ControllerImage.onWheel(controllerImage, event); }
      self.div.onmouseleave = function (event) { ControllerImage.onMouseLeave(controllerImage, event); }
      self.div.onmousemove = function (event) { ControllerImage.onMouseMove(controllerImage, event); }
      self.div.onkeydown = function (event) { ControllerImage.onKeyDown(controllerImage, event); }
    } else if (mode == 'non-interactive') {
      self.div.onmousedown = null;
      self.div.onwheel = null;
      self.div.onmouseleave = null;
      self.div.onmousemove = null;
      self.div.onkeydown = null;
    } else if (mode == 'demo') {
      const prevMode = self.mode;
      const returnToPrevMode = function (event) { ControllerImage.setMode(self, prevMode); };
      self.div.onmousedown = returnToPrevMode;
      self.div.onwheel = returnToPrevMode;
      self.div.onmouseleave = returnToPrevMode;
      self.div.onmousemove = returnToPrevMode;
      self.div.onkeydown = returnToPrevMode;
      const interval = modeOptions.interval || 333;
      self.demoTimer = setInterval(function () { self.randomlyChangeARandomSlot(); }, interval);
    } else {
      throw new RangeError("Invalid mode for ControllerImage.setMode: " + mode);
    }
    self.mode = mode;
  }

  static onClick(self, event) {
    const coords = self.pixelCoordsFromMouseEvent(event);
    self.setSelectedSlot(self.closestSlot(coords.x, coords.y));
    self.incrementSelectedSlotValue();
  }

  static onWheel(self, event) {
    // TODO: Take the wheel/scroll amount into account...
    const coords = self.pixelCoordsFromMouseEvent(event);
    const slotIndex = self.closestSlot(coords.x, coords.y);
    self.setSelectedSlot(slotIndex);
    self.incrementSelectedSlotValue();
    if (slotIndex !== null) {
      event.preventDefault();
    }
  }

  static onMouseLeave(self, event) {
    self.setSelectedSlot(null);
  }

  static onMouseMove(self, event) {
    // TODO: Take the wheel/scroll amount into account...
    const coords = self.pixelCoordsFromMouseEvent(event);
    self.setSelectedSlot(self.closestSlot(coords.x, coords.y));
  }

  static onKeyDown(self, event) {
    const k = event.key;
    if (k == " " || k == "Enter" || k == "ArrowDown" || k == "s") {
      self.incrementSelectedSlotValue();
      event.preventDefault();
    } else if (k == "ArrowUp" || k == "w") {
      self.decrementSelectedSlotValue();
      event.preventDefault();
    } else if (k == "ArrowLeft" || (k == "Tab" && event.shiftKey) || k == "a") {
      self.decrementSelectedSlot();
      event.preventDefault();
    } else if (k == "ArrowRight" || (k == "Tab" && !event.shiftKey) || k == "d") {
      self.incrementSelectedSlot();
      event.preventDefault();
    }
  }
}

let controllerImage = new ControllerImage("controllerImageDiv", "https://mikelmcdaniel.github.io/controller_demo/");
ControllerImage.setMode(controllerImage, 'demo', { interval: 700});
