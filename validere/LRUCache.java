import java.util.*;

public class LRUCache {

	static int cacheSize = 3;

    public static void main(String[] args) {
        System.out.println("LRUCache");

//		myCache = lruCache(cacheSize);
		Map<Integer,String> cache = lruCache(3);
		System.out.println("All Candidates for Junit testing\n");
		
		System.out.println("testing initial cache empty: " + 
			((cache.size() == 0) ? "passed" : " failed" ));
				
		System.out.println("testing get on non-existent key: " + 
			((cache.get(100) == null) ? "passed" : " failed" ));
			
		cache.put(100,"zero");
		   
		System.out.println("testing get on existent key: " + 
			((cache.get(100) != null) ? "passed" : " failed" ));		
		 
   		cache.put(101, "one");  
   		cache.put(102, "two");

		System.out.println("testing cache full: " + 
			((cache.size() == cacheSize) ? "passed" : " failed" ));
   					
   		//making 102 least recently used by accessing others
   		cache.get(100);
   		cache.get(101);
		//insert a new element  		
   		cache.put(103, "three");  
   		
   		System.out.println("adding new k,v doesn't change size of cache: " + 
			((cache.size() == cacheSize) ? "passed" : " failed" ));
   		   		
		// confirm 102 is evicted with the new insertion
		System.out.println("insert a new element and confirm 102 is evicted: " + 
			((cache.get(102) == null) ? "passed" : " failed" ));
		
  		// accessing same elements does not lead to any eviction
		Set<Integer> setOfKeys = cache.keySet();
		cache.get(101);
		cache.get(101);
		System.out.println("accessing same elements does not lead to any eviction: " + 
			(setOfKeys.equals(cache.keySet()) ? "passed" : " failed" ));

		//System.out.println("setOfKeys: " + setOfKeys);
		//System.out.println("cache.keySet(): " + cache.keySet());
		
		// confirm order of elements changes when elements are accesses
		//List<Integer> LRUOrder = new ArrayList<>(target.keySet());
		List<Integer> oldOrder = new ArrayList<>(cache.keySet());
		System.out.println("oldOrder: " + oldOrder);

		cache.get(100);
		
		List<Integer> LRUOrder = new ArrayList<>(cache.keySet());
		System.out.println("LRUOrder: " + LRUOrder);
	
		System.out.println("order of elements changes when elements are accesses: " + 
			(!oldOrder.equals(LRUOrder) ? "passed" : " failed" ));		

		// confirm order of elements is from lru to mru		
   		  
		List<Integer> expectedLRUOrder = new ArrayList<Integer>();
		expectedLRUOrder.add(103);
		expectedLRUOrder.add(101);
		expectedLRUOrder.add(100);

		System.out.println("confirm order of elements is from lru to mru: " + 
			(expectedLRUOrder.equals(LRUOrder) ? "passed" : " failed" ));
    }

	public static Map<Integer,String> lruCache(final int maxSize) {		
    	return new LinkedHashMap<Integer,String>(maxSize, 0.75f, true) {
        	@Override
        	protected boolean removeEldestEntry(Map.Entry<Integer,String> eldest) {
            	return size() > maxSize;
        	}
        	
   		};
	}
	
	
}
