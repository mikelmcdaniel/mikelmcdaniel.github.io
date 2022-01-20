class ControllerImage {
  // moduleValues is used to map to files.
  // moduleValues specifies which types of things can go in that module.
  moduleValues = [
    ["CB1", "CB2", "CB3", "CB4", "CB5", "CB6", "CB7", "CB8", "CB9"],
    ["DP1", "FB1", "JS1"],
    ["DP2", "FB2", "JS2"],
    ["DP3", "FB3", "JS3"],
    ["DP4", "FB4", "JS4"],
    ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "PC7", "PC8", "PC9","PC10", "PC11", "PC12"]];
  // TODO: It would be nice if these didn't need to be hard-coded...
  // moduleCoords and maxModuleRadius are used for mapping a 2d point to
  // the nearest module (for UI purposes).
  moduleCoords = [
    { x: null, y: null },
    { x: 336, y: 154 },
    { x: 336, y: 334 },
    { x: 520, y: 456 },
    { x: 766, y: 372 },
    { x: 520, y: 200 }];
  maxModuleRadius = 150;

  // Stateful UI
  // selectedModule is null when no module is selected.
  // Any functions using selectedModule should handle null!
  selectedModule = null;
  mode = null;
  demoTimer = null;

  div = null;
  baseImg = null;
  moduleImgs = null;
  moduleIndices = null;

  constructor(divID, imgRootURL="") {
    this.imgRootURL = imgRootURL;
    this.div = document.getElementById(divID);

    // Initialize module info from HTML.
    this.moduleImgs = [];
    this.moduleIndices = [];
    for (let mi = 0; mi < this.moduleValues.length; ++mi) {
      let img = document.getElementById(this.div.id + ".module" + mi);
      this.moduleImgs.push(img);
      let indices = this.indicesFromImgSrc(img.src);
      console.assert(indices.moduleIndex == mi);
      this.moduleIndices.push(indices.moduleValueIndex);
      // Ensure HTML is using the same exact imgSrc, that will be used when the modules are changed!
      // This isn't necessary but helps catch bugs sooner.
      console.assert(this.moduleImgs[mi].src == this.imgSrc(mi, this.moduleIndices[mi]));
    }
    this.baseImg = this.moduleImgs[0];
    ControllerImage.setMode(this, 'interactive');
  }

  imgSrcBaseName(moduleIndex, moduleValueIndex) {
    return this.moduleValues[moduleIndex][moduleValueIndex] + ".png";
  }

  imgSrc(moduleIndex, moduleValueIndex) {
    return this.imgRootURL + this.imgSrcBaseName(moduleIndex, moduleValueIndex);
  }

  static baseName(urlStr) {
    const url = new URL(urlStr);
    const urlParts = url.pathname.split("/");
    return urlParts[urlParts.length - 1];
  }

  indicesFromImgSrc(imgSrc) {
    const imgSrcBaseName = ControllerImage.baseName(imgSrc)
    // TODO: This could be more efficient!
    for (let mi = 0; mi < this.moduleValues.length; ++mi) {
      for (let mvi = 0; mvi < this.moduleValues[mi].length; ++mvi) {
        if (this.imgSrcBaseName(mi, mvi) == imgSrcBaseName) {
          return { moduleIndex: mi, moduleValueIndex: mvi };
        }
      }
    }
    throw new RangeError("Could not determine modules for " + imgSrc);
  }

  closestModule(pixelX, pixelY) {
    let moduleIndex = 0;
    let closestDistance = Infinity;
    for (let mi = 0; mi < this.moduleCoords.length; ++mi) {
      const cx = this.moduleCoords[mi].x;
      const cy = this.moduleCoords[mi].y;
      const d = Math.sqrt(Math.pow(pixelX - cx, 2) + Math.pow(pixelY - cy, 2));
      if (d < closestDistance) {
        moduleIndex = mi;
        closestDistance = d;
      }
    }
    return closestDistance <= this.maxModuleRadius ? moduleIndex : 0;
  }

  // Change what's in a given module.
  // e.g. incrementModuleValue(0) might change module 0 from a D-Pad to a Joy Stick.
  setModule(moduleIndex, moduleValueIndex) {
    if (moduleIndex === null) {
      return;
    }
    this.moduleIndices[moduleIndex] = moduleValueIndex;
    this.moduleImgs[moduleIndex].src = this.imgSrc(moduleIndex, moduleValueIndex);

    // TODO: Allow face plate and module colors to be selected independently.
    // This hack keeps them in sync with the controller base color.
    if (moduleIndex == 0) {
      document.getElementById(this.div.id + ".moduleColor").src = this.moduleImgs[moduleIndex].src.replace("/CB", "/MC");
    }
  }

  incrementModuleValue(moduleIndex) {
    if (moduleIndex === null) {
      return;
    }
    const newModuleValueIndex = (this.moduleIndices[moduleIndex] + 1) % this.moduleValues[moduleIndex].length;
    this.setModule(moduleIndex, newModuleValueIndex);
  }

  decrementModuleValue(moduleIndex) {
    if (moduleIndex === null) {
      return;
    }
    const newModuleValueIndex = (this.moduleIndices[moduleIndex] + this.moduleValues[moduleIndex].length - 1) % this.moduleValues[moduleIndex].length;
    this.setModule(moduleIndex, newModuleValueIndex);
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

  highlightSelectedModule() {
    if (this.selectedModule === null) {
      for (let mi = 0; mi < this.moduleImgs.length; ++mi) {
        this.moduleImgs[mi].style.opacity = 1.0;
      }
      // TODO: Allow face plate and module colors to be selected independently.
      // This hack keeps them in sync with the controller base color.
      document.getElementById(this.div.id + ".moduleColor").style.opacity = 1.0;
    } else {
      for (let mi = 0; mi < this.moduleImgs.length; ++mi) {
        this.moduleImgs[mi].style.opacity = 0.5;
      }
      // TODO: Allow face plate and module colors to be selected independently.
      // This hack keeps them in sync with the controller base color.
      if (this.selectedModule == 0) {
        document.getElementById(this.div.id + ".moduleColor").style.opacity = 1.0;
      } else {
        document.getElementById(this.div.id + ".moduleColor").style.opacity = 0.5;
      }
      this.moduleImgs[this.selectedModule].style.opacity = 1.0;
    }
  }

  setSelectedModule(selectedModuleIndex) {
    this.selectedModule = selectedModuleIndex;
    this.highlightSelectedModule();
  }

  incrementSelectedModuleValue() {
    this.incrementModuleValue(this.selectedModule);
  }

  decrementSelectedModuleValue() {
    this.decrementModuleValue(this.selectedModule);
  }

  incrementSelectedModule() {
    this.setSelectedModule((this.selectedModule + 1) % this.moduleValues.length);
  }

  decrementSelectedModule() {
    this.setSelectedModule((this.selectedModule + numModules - 1) % numModules);
  }

  randomlyChangeARandomModule() {
    const numModules = this.moduleValues.length;
    const randomModule = Math.floor(Math.random() * numModules);
    const numModuleValues = this.moduleValues[randomModule].length;
    const randomModuleValue = (this.moduleIndices[randomModule] + Math.floor(Math.random() * (numModuleValues - 1)) + 1) % numModuleValues;
    this.setModule(randomModule, randomModuleValue);
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
      self.demoTimer = setInterval(function () { self.randomlyChangeARandomModule(); }, interval);
    } else {
      throw new RangeError("Invalid mode for ControllerImage.setMode: " + mode);
    }
    self.mode = mode;
  }

  static onClick(self, event) {
    const coords = self.pixelCoordsFromMouseEvent(event);
    self.setSelectedModule(self.closestModule(coords.x, coords.y));
    self.incrementSelectedModuleValue();
  }

  static onWheel(self, event) {
    // TODO: Take the wheel/scroll amount into account...
    const coords = self.pixelCoordsFromMouseEvent(event);
    const moduleIndex = self.closestModule(coords.x, coords.y);
    self.setSelectedModule(moduleIndex);
    self.incrementSelectedModuleValue();
    if (moduleIndex !== null) {
      event.preventDefault();
    }
  }

  static onMouseLeave(self, event) {
    self.setSelectedModule(null);
  }

  static onMouseMove(self, event) {
    // TODO: Take the wheel/scroll amount into account...
    const coords = self.pixelCoordsFromMouseEvent(event);
    self.setSelectedModule(self.closestModule(coords.x, coords.y));
  }

  static onKeyDown(self, event) {
    const k = event.key;
    if (k == " " || k == "Enter" || k == "ArrowDown" || k == "s") {
      self.incrementSelectedModuleValue();
      event.preventDefault();
    } else if (k == "ArrowUp" || k == "w") {
      self.decrementSelectedModuleValue();
      event.preventDefault();
    } else if (k == "ArrowLeft" || (k == "Tab" && event.shiftKey) || k == "a") {
      self.decrementSelectedModule();
      event.preventDefault();
    } else if (k == "ArrowRight" || (k == "Tab" && !event.shiftKey) || k == "d") {
      self.incrementSelectedModule();
      event.preventDefault();
    }
  }
}

let controllerImage = new ControllerImage("controllerImageDiv", "imgs/");
ControllerImage.setMode(controllerImage, 'demo', { interval: 700});
