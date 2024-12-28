package thelaststand.app.game.data.notification
{
   import org.osflash.signals.Signal;
   import thelaststand.app.game.gui.dialogues.EventAlertDialogue;
   import thelaststand.app.gui.dialogues.BaseDialogue;
   import thelaststand.common.gui.dialogues.Dialogue;
   import thelaststand.common.lang.Language;
   
   public class AllianceDisbandedNotification implements INotification
   {
      private var _active:Boolean = true;
      
      private var _closed:Signal;
      
      private var _data:Object;
      
      public function AllianceDisbandedNotification(param1:Object)
      {
         super();
         this._closed = new Signal(INotification);
         this._data = param1;
      }
      
      public function open() : void
      {
         var allianceName:String;
         var allianceId:String;
         var lang:Language;
         var dlg:EventAlertDialogue;
         var thisRef:INotification = null;
         if(this._data == null)
         {
            this._closed.dispatch(this);
            return;
         }
         allianceName = !!this._data.hasOwnProperty("allianceName") ? this._data.allianceName : "";
         allianceId = !!this._data.hasOwnProperty("allianceId") ? this._data.allianceId : "";
         thisRef = this;
         lang = Language.getInstance();
         dlg = new EventAlertDialogue("images/alliances/alliance-disbanded.jpg",110,110,"left","alliance-disbanded");
         dlg.addTitle(lang.getString("alliance_disbanded_title"),BaseDialogue.TITLE_COLOR_GREY);
         dlg.addBody(lang.getString("alliance_disbanded_msg",allianceName));
         dlg.addButton(lang.getString("alliance_disbanded_ok"),true,{"width":90});
         dlg.closed.addOnce(function(param1:Dialogue):void
         {
            _closed.dispatch(thisRef);
         });
         dlg.open();
      }
      
      public function get active() : Boolean
      {
         return this._active;
      }
      
      public function set active(param1:Boolean) : void
      {
         this._active = param1;
      }
      
      public function get closed() : Signal
      {
         return this._closed;
      }
      
      public function get type() : String
      {
         return NotificationType.ALLIANCE_DISBANDED;
      }
      
      public function get data() : *
      {
         return this._data;
      }
   }
}

