package thelaststand.app.game.gui.mission
{
   import alternativa.engine3d.core.BoundBox;
   import flash.display.Bitmap;
   import flash.display.Shape;
   import flash.display.Sprite;
   import flash.events.Event;
   import flash.geom.Point;
   import flash.geom.Vector3D;
   import thelaststand.app.display.Effects;
   import thelaststand.app.game.data.Survivor;
   import thelaststand.app.game.entities.actors.Actor;
   import thelaststand.app.game.logic.ai.states.ActorScavengeState;
   import thelaststand.engine.objects.GameEntity;
   import thelaststand.engine.utils.BoundingBoxUtils;
   
   public class UISearchProgress extends Sprite
   {
      private var _barBuffer:int = 6;
      
      private var _width:int = 36;
      
      private var _height:int = 5;
      
      private var _survivor:Survivor;
      
      private var _targetPos:Vector3D = new Vector3D();
      
      private var mc_bar:Shape;
      
      private var mc_track:Shape;
      
      private var bmp_icon:Bitmap;
      
      public var entity:GameEntity;
      
      public function UISearchProgress(param1:Survivor, param2:GameEntity)
      {
         super();
         mouseEnabled = mouseChildren = false;
         this._survivor = param1;
         this.entity = param2;
         this.visible = true;
         this.mc_track = new Shape();
         this.mc_track.graphics.beginFill(4752805,0.5);
         this.mc_track.graphics.drawRect(0,0,this._width,this._height);
         this.mc_track.graphics.endFill();
         this.mc_track.filters = [Effects.STROKE];
         this.mc_bar = new Shape();
         this.mc_bar.graphics.beginFill(16777215,1);
         this.mc_bar.graphics.drawRect(0,0,this._width,this._height);
         this.mc_bar.graphics.endFill();
         this.bmp_icon = new Bitmap(new BmpIconSearchTimer());
         this.bmp_icon.x = -int(this.bmp_icon.width * 0.5);
         this.bmp_icon.y = -int(this.bmp_icon.height * 0.5) + 2;
         this._barBuffer = int(this.bmp_icon.width * 0.5);
         addChild(this.mc_track);
         addChild(this.mc_bar);
         addChild(this.bmp_icon);
         addEventListener(Event.ADDED_TO_STAGE,this.onAddedToStage,false,0,true);
         addEventListener(Event.REMOVED_FROM_STAGE,this.onRemovedFromStage,false,0,true);
      }
      
      public function dispose() : void
      {
         if(parent)
         {
            parent.removeChild(this);
         }
         removeEventListener(Event.ADDED_TO_STAGE,this.onAddedToStage);
         removeEventListener(Event.REMOVED_FROM_STAGE,this.onRemovedFromStage);
         this.bmp_icon.bitmapData.dispose();
         this.bmp_icon.bitmapData = null;
         this.bmp_icon = null;
         this.mc_track.filters = [];
         this.mc_track = null;
         this.entity = null;
         this._survivor = null;
         this._targetPos = null;
      }
      
      private function calculate3DPosition() : void
      {
         if(this.entity == null || this.entity.scene == null || this.entity.asset == null)
         {
            return;
         }
         var _loc1_:BoundBox = new BoundBox();
         BoundingBoxUtils.transformBounds(this.entity.asset,this.entity.asset.matrix,_loc1_);
         var _loc2_:Number = _loc1_.maxX - _loc1_.minX;
         var _loc3_:Number = _loc1_.maxY - _loc1_.minY;
         var _loc4_:Number = _loc1_.maxZ - _loc1_.minZ;
         this._targetPos.x = this.entity.transform.position.x + _loc1_.minX + _loc2_ * 0.5;
         this._targetPos.y = this.entity.transform.position.y + _loc1_.minY + _loc3_ * 0.5;
         this._targetPos.z = this.entity.transform.position.z + _loc1_.minZ + _loc4_ * 0.5;
      }
      
      private function onAddedToStage(param1:Event) : void
      {
         addEventListener(Event.ENTER_FRAME,this.onEnterFrame,false,0,true);
         this.calculate3DPosition();
         this.onEnterFrame(null);
      }
      
      private function onRemovedFromStage(param1:Event) : void
      {
         removeEventListener(Event.ENTER_FRAME,this.onEnterFrame);
      }
      
      private function onEnterFrame(param1:Event) : void
      {
         var _loc3_:ActorScavengeState = null;
         if(this.entity == null || this.entity.scene == null || this.entity.asset == null)
         {
            return;
         }
         var _loc2_:Actor = this._survivor.actor;
         _loc3_ = this._survivor.stateMachine.state as ActorScavengeState;
         if(_loc2_.scene == null || _loc3_ == null)
         {
            if(parent != null)
            {
               parent.removeChild(this);
            }
            return;
         }
         var _loc4_:Point = _loc2_.scene.getScreenPosition(this._targetPos.x,this._targetPos.y,this._targetPos.z);
         x = int(_loc4_.x - this._width * 0.5);
         y = int(_loc4_.y - this._height);
         this.mc_bar.width = this._barBuffer + (this._width - this._barBuffer) * _loc3_.progress;
      }
   }
}

