package versions.version2.a3d.objects
{
   import alternativa.types.Long;
   
   public class A3D2Mesh
   {
      private var _boundBoxId:int;
      
      private var _id:Long;
      
      private var _indexBufferId:int;
      
      private var _name:String;
      
      private var _parentId:Long;
      
      private var _surfaces:Vector.<A3D2Surface>;
      
      private var _transform:A3D2Transform;
      
      private var _vertexBuffers:Vector.<int>;
      
      private var _visible:Boolean;
      
      public function A3D2Mesh(param1:int, param2:Long, param3:int, param4:String, param5:Long, param6:Vector.<A3D2Surface>, param7:A3D2Transform, param8:Vector.<int>, param9:Boolean)
      {
         super();
         this._boundBoxId = param1;
         this._id = param2;
         this._indexBufferId = param3;
         this._name = param4;
         this._parentId = param5;
         this._surfaces = param6;
         this._transform = param7;
         this._vertexBuffers = param8;
         this._visible = param9;
      }
      
      public function get boundBoxId() : int
      {
         return this._boundBoxId;
      }
      
      public function set boundBoxId(param1:int) : void
      {
         this._boundBoxId = param1;
      }
      
      public function get id() : Long
      {
         return this._id;
      }
      
      public function set id(param1:Long) : void
      {
         this._id = param1;
      }
      
      public function get indexBufferId() : int
      {
         return this._indexBufferId;
      }
      
      public function set indexBufferId(param1:int) : void
      {
         this._indexBufferId = param1;
      }
      
      public function get name() : String
      {
         return this._name;
      }
      
      public function set name(param1:String) : void
      {
         this._name = param1;
      }
      
      public function get parentId() : Long
      {
         return this._parentId;
      }
      
      public function set parentId(param1:Long) : void
      {
         this._parentId = param1;
      }
      
      public function get surfaces() : Vector.<A3D2Surface>
      {
         return this._surfaces;
      }
      
      public function set surfaces(param1:Vector.<A3D2Surface>) : void
      {
         this._surfaces = param1;
      }
      
      public function get transform() : A3D2Transform
      {
         return this._transform;
      }
      
      public function set transform(param1:A3D2Transform) : void
      {
         this._transform = param1;
      }
      
      public function get vertexBuffers() : Vector.<int>
      {
         return this._vertexBuffers;
      }
      
      public function set vertexBuffers(param1:Vector.<int>) : void
      {
         this._vertexBuffers = param1;
      }
      
      public function get visible() : Boolean
      {
         return this._visible;
      }
      
      public function set visible(param1:Boolean) : void
      {
         this._visible = param1;
      }
      
      public function toString() : String
      {
         var _loc1_:String = "A3D2Mesh [";
         _loc1_ += "boundBoxId = " + this.boundBoxId + " ";
         _loc1_ += "id = " + this.id + " ";
         _loc1_ += "indexBufferId = " + this.indexBufferId + " ";
         _loc1_ += "name = " + this.name + " ";
         _loc1_ += "parentId = " + this.parentId + " ";
         _loc1_ += "surfaces = " + this.surfaces + " ";
         _loc1_ += "transform = " + this.transform + " ";
         _loc1_ += "vertexBuffers = " + this.vertexBuffers + " ";
         _loc1_ += "visible = " + this.visible + " ";
         return _loc1_ + "]";
      }
   }
}

